package main

import (
	"database/sql"
	"fmt"
	"hash/fnv"
	"log"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"unicode"

	_ "github.com/mattn/go-sqlite3"
)

type MapTask struct {
	M, R       int    // total number of map and reduce tasks
	N          int    // map task number, 0-based
	SourceHost string // address of host with map input file
}

type ReduceTask struct {
	M, R        int      // total number of map and reduce tasks
	N           int      // reduce task number, 0-based
	SourceHosts []string // addresses of map workers
}

type Pair struct {
	Key   string
	Value string
}

type Interface interface {
	Map(key, value string, output chan<- Pair) error
	Reduce(key string, values <-chan string, output chan<- Pair) error
}

func mapSourceFile(m int) string       { return fmt.Sprintf("map_%d_source.db", m) }
func mapInputFile(m int) string        { return fmt.Sprintf("map_%d_input.db", m) }
func mapOutputFile(m, r int) string    { return fmt.Sprintf("map_%d_output_%d.db", m, r) }
func reduceInputFile(r int) string     { return fmt.Sprintf("reduce_%d_input.db", r) }
func reduceOutputFile(r int) string    { return fmt.Sprintf("reduce_%d_output.db", r) }
func reducePartialFile(r int) string   { return fmt.Sprintf("reduce_%d_partial.db", r) }
func reduceTempFile(r int) string      { return fmt.Sprintf("reduce_%d_temp.db", r) }
func makeURL(host, file string) string { return fmt.Sprintf("http://%s/data/%s", host, file) }

func getLocalAddress() string {
	conn, err := net.Dial("udp", "8.8.8.8:80")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	localAddr := conn.LocalAddr().(*net.UDPAddr)

	localaddress := localAddr.IP.String()

	if localaddress == "" {
		panic("init: failed to find non-loopback interface with valid address on this node")
	}
	return localaddress
}

type Client struct{}

func (c Client) Map(key, value string, output chan<- Pair) error {
	defer close(output)
	lst := strings.Fields(value)
	for _, elt := range lst {
		word := strings.Map(func(r rune) rune {
			if unicode.IsLetter(r) || unicode.IsDigit(r) {
				return unicode.ToLower(r)
			}
			return -1
		}, elt)
		if len(word) > 0 {
			output <- Pair{Key: word, Value: "1"}
		}
	}
	return nil
}

func (c Client) Reduce(key string, values <-chan string, output chan<- Pair) error {
	defer close(output)
	count := 0
	for v := range values {
		i, err := strconv.Atoi(v)
		if err != nil {
			return err
		}
		count += i
	}
	p := Pair{Key: key, Value: strconv.Itoa(count)}
	output <- p
	return nil
}

func (task *MapTask) Process(tempdir string, client Interface) error {
	// Step 1: Download the source file
	url := makeURL(task.SourceHost, mapSourceFile(task.N))
	inputPath := filepath.Join(tempdir, mapInputFile(task.N))
	if err := download(url, inputPath); err != nil {
		return fmt.Errorf("failed to download input file: %w", err)
	}

	// Step 2: Open the input DB
	db, err := openDatabase(inputPath)
	if err != nil {
		return fmt.Errorf("failed to open input database: %w", err)
	}
	defer db.Close()

	// Step 3: Create output DBs and prepared statements
	outs := make([]*sql.DB, task.R)
	inserts := make([]*sql.Stmt, task.R)
	for r := 0; r < task.R; r++ {
		path := filepath.Join(tempdir, mapOutputFile(task.N, r))
		out, err := createDatabase(path)
		if err != nil {
			return fmt.Errorf("failed to create output DB for reducer %d: %w", r, err)
		}
		outs[r] = out
		stmt, err := out.Prepare("insert into pairs (key, value) values (?, ?)")
		if err != nil {
			return fmt.Errorf("failed to prepare insert for reducer %d: %w", r, err)
		}
		inserts[r] = stmt
	}
	defer func() {
		for _, stmt := range inserts {
			if stmt != nil {
				stmt.Close()
			}
		}
		for _, db := range outs {
			if db != nil {
				db.Close()
			}
		}
	}()

	// Step 4: Read from input DB
	rows, err := db.Query("select key, value from pairs")
	if err != nil {
		return fmt.Errorf("querying input: %w", err)
	}
	defer rows.Close()

	inputCount := 0
	outputCount := 0
	for rows.Next() {
		var key, value string
		if err := rows.Scan(&key, &value); err != nil {
			return fmt.Errorf("scanning input: %w", err)
		}
		inputCount++

		// Call client.Map
		ch := make(chan Pair, 100)
		err := client.Map(key, value, ch)
		if err != nil {
			return fmt.Errorf("client.Map error: %w", err)
		}
		for pair := range ch {
			hash := fnv.New32()
			hash.Write([]byte(pair.Key))
			r := int(hash.Sum32() % uint32(task.R))
			if _, err := inserts[r].Exec(pair.Key, pair.Value); err != nil {
				return fmt.Errorf("inserting pair into reducer %d: %w", r, err)
			}
			outputCount++
		}
	}
	if err := rows.Err(); err != nil {
		return fmt.Errorf("row iteration error: %w", err)
	}

	log.Printf("map task %d processed %d pairs, generated %d pairs", task.N, inputCount, outputCount)
	return nil
}

func (task *ReduceTask) Process(tempdir string, client Interface) error {
	// Step 1: gather all map outputs for this reducer
	var urls []string
	for m := 0; m < task.M; m++ {
		file := mapOutputFile(m, task.N)
		urls = append(urls, makeURL(task.SourceHosts[m], file))
	}
	inputPath := filepath.Join(tempdir, reduceInputFile(task.N))
	db, err := mergeDatabases(urls, inputPath, reduceTempFile(task.N))
	if err != nil {
		return fmt.Errorf("mergeDatabases failed: %w", err)
	}
	defer db.Close()

	// Step 2: create output DB and prepare insert
	outPath := filepath.Join(tempdir, reduceOutputFile(task.N))
	outDB, err := createDatabase(outPath)
	if err != nil {
		return fmt.Errorf("create output database: %w", err)
	}
	defer outDB.Close()
	stmt, err := outDB.Prepare("insert into pairs (key, value) values (?, ?)")
	if err != nil {
		return fmt.Errorf("prepare insert: %w", err)
	}
	defer stmt.Close()

	// Step 3: read and reduce sorted pairs
	rows, err := db.Query("select key, value from pairs order by key, value")
	if err != nil {
		return fmt.Errorf("query input db: %w", err)
	}
	defer rows.Close()

	var (
		currentKey            string
		inputChan             chan string
		outputChan            chan Pair
		done                  chan error
		keys, values, outputs int
	)
	flush := func() error {
		if inputChan != nil {
			close(inputChan)
			err := <-done
			if err != nil {
				return fmt.Errorf("client.Reduce failed: %w", err)
			}
			for pair := range outputChan {
				if _, err := stmt.Exec(pair.Key, pair.Value); err != nil {
					return fmt.Errorf("insert reduce result: %w", err)
				}
				outputs++
			}
		}
		return nil
	}
	for rows.Next() {
		var key, value string
		if err := rows.Scan(&key, &value); err != nil {
			return fmt.Errorf("scan: %w", err)
		}
		values++
		if key != currentKey {
			if err := flush(); err != nil {
				return err
			}
			currentKey = key
			inputChan = make(chan string, 100)
			outputChan = make(chan Pair, 100)
			done = make(chan error, 1)
			go func(k string, in <-chan string, out chan<- Pair) {
				done <- client.Reduce(k, in, out)
			}(key, inputChan, outputChan)
			keys++
		}
		inputChan <- value
	}
	if err := flush(); err != nil {
		return err
	}
	if err := rows.Err(); err != nil {
		return fmt.Errorf("row iteration error: %w", err)
	}

	log.Printf("reduce task %d processed %d keys and %d values, generated %d pairs", task.N, keys, values, outputs)
	return nil
}

func main() {
	m := 10
	r := 5
	source := "source.db"
	//target := "target.db"
	tmp := os.TempDir()

	tempdir := filepath.Join(tmp, fmt.Sprintf("mapreduce.%d", os.Getpid()))
	if err := os.RemoveAll(tempdir); err != nil {
		log.Fatalf("unable to delete old temp dir: %v", err)
	}
	if err := os.Mkdir(tempdir, 0700); err != nil {
		log.Fatalf("unable to create temp dir: %v", err)
	}
	defer os.RemoveAll(tempdir)

	log.Printf("splitting %s into %d pieces", source, m)
	var paths []string
	for i := 0; i < m; i++ {
		paths = append(paths, filepath.Join(tempdir, mapSourceFile(i)))
	}
	if err := splitDatabase(source, paths); err != nil {
		log.Fatalf("splitting database: %v", err)
	}

	myAddress := net.JoinHostPort(getLocalAddress(), "3410")
	log.Printf("starting http server at %s", myAddress)
	http.Handle("/data/", http.StripPrefix("/data", http.FileServer(http.Dir(tempdir))))

	// bind on the port before launching the background goroutine on Serve
	// to prevent race condition with call to download below
	listener, err := net.Listen("tcp", myAddress)
	if err != nil {
		log.Fatalf("Listen error on address %s: %v", myAddress, err)
	}
	go func() {
		if err := http.Serve(listener, nil); err != nil {
			log.Fatalf("Serve error: %v", err)
		}
	}()

	// build the map tasks
	var mapTasks []*MapTask
	for i := 0; i < m; i++ {
		task := &MapTask{
			M:          m,
			R:          r,
			N:          i,
			SourceHost: myAddress,
		}
		mapTasks = append(mapTasks, task)
	}

	// build the reduce tasks
	var reduceTasks []*ReduceTask
	for i := 0; i < r; i++ {
		task := &ReduceTask{
			M:           m,
			R:           r,
			N:           i,
			SourceHosts: make([]string, m),
		}
		reduceTasks = append(reduceTasks, task)
	}

	var client Client

	// process the map tasks
	for i, task := range mapTasks {
		if err := task.Process(tempdir, client); err != nil {
			log.Fatalf("processing map task %d: %v", i, err)
		}
		for _, reduce := range reduceTasks {
			reduce.SourceHosts[i] = myAddress
		}
	}

	// process the reduce tasks
	for i, task := range reduceTasks {
		if err := task.Process(tempdir, client); err != nil {
			log.Fatalf("processing reduce task %d: %v", i, err)
		}
	}

	// gather outputs into final target.db file
	var outputURLs []string
	for i := 0; i < r; i++ {
		file := reduceOutputFile(i)
		outputURLs = append(outputURLs, makeURL(myAddress, file))
	}
	finalPath := filepath.Join(tempdir, "target.db")
	finalTemp := filepath.Join(tempdir, "target_temp.db")

	db, err := mergeDatabases(outputURLs, finalPath, finalTemp)
	if err != nil {
		log.Fatalf("final merge failed: %v", err)
	}
	defer db.Close()

	var total int
	err = db.QueryRow("select count(1) from pairs").Scan(&total)
	if err != nil {
		log.Fatalf("counting final output rows: %v", err)
	}
	log.Printf("final output database contains %d rows", total)

	// show top 20 most frequent words
	rows, err := db.Query("select key, value from pairs order by cast(value as int) desc limit 20")
	if err != nil {
		log.Fatalf("query top results: %v", err)
	}
	defer rows.Close()
	log.Println("Top 20 words:")
	for rows.Next() {
		var key, val string
		rows.Scan(&key, &val)
		log.Printf("%s: %s", key, val)
	}
}
