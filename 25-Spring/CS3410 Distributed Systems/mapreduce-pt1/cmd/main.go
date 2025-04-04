package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"

	"mapreduce"
)

func testOpenDatabase() {
	// Test on austen.db using the function from the same package.
	db, err := mapreduce.OpenDatabase("austen.db")
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer db.Close()

	var count int
	err = db.QueryRow("select count(1) from pairs").Scan(&count)
	if err != nil {
		log.Fatalf("Query error: %v", err)
	}
	fmt.Printf("austen.db contains %d rows in the pairs table.\n", count)
}

func testCreateDatabase() {
	path := "test.db"
	os.Remove(path) // Clean up previous test file

	db, err := mapreduce.CreateDatabase(path)
	if err != nil {
		log.Fatalf("Failed to create database: %v", err)
	}
	defer db.Close()

	// Check if the table exists by querying sqlite_master
	var name string
	err = db.QueryRow("SELECT name FROM sqlite_master WHERE type='table' AND name='pairs'").Scan(&name)
	if err != nil && err != sql.ErrNoRows {
		log.Fatalf("Error checking for table: %v", err)
	}
	if name != "pairs" {
		log.Fatalf("Table 'pairs' not found in created database")
	}
	fmt.Println("test.db created successfully with table 'pairs'.")
}

func testSplitDatabase() {
	// Define output paths
	outputFiles := []string{"austen-0.db", "austen-1.db", "austen-2.db"}

	// Remove any existing files for a clean test
	for _, f := range outputFiles {
		os.Remove(f)
	}

	// Split the input database
	err := mapreduce.SplitDatabase("austen.db", outputFiles)
	if err != nil {
		log.Fatalf("mapreduce.SplitDatabase failed: %v", err)
	}

	// Print out row counts for each split file
	total := 0
	for _, f := range outputFiles {
		db, err := mapreduce.OpenDatabase(f)
		if err != nil {
			log.Fatalf("Failed to open split database %s: %v", f, err)
		}
		var count int
		err = db.QueryRow("select count(1) from pairs").Scan(&count)
		if err != nil {
			log.Fatalf("Query error on %s: %v", f, err)
		}
		fmt.Printf("%s contains %d rows.\n", f, count)
		total += count
		db.Close()
	}
	fmt.Printf("Total rows in all split databases: %d\n", total)
}

func testMergeDatabases() {
	urls := []string{
		"http://localhost:8080/data/austen-0.db",
		"http://localhost:8080/data/austen-1.db",
		"http://localhost:8080/data/austen-2.db",
	}

	mergedPath := "austen-merged.db"
	tempFile := "temp.db"

	db, err := mapreduce.MergeDatabases(urls, mergedPath, tempFile)
	if err != nil {
		log.Fatalf("MergeDatabases failed: %v", err)
	}
	defer db.Close()

	var count int
	err = db.QueryRow("select count(1) from pairs").Scan(&count)
	if err != nil {
		log.Fatalf("Query error on merged db: %v", err)
	}
	fmt.Printf("Merged database contains %d rows.\n", count)
}

func main() {
	// Start local web server for merge testing
	go func() {
		http.Handle("/data/", http.StripPrefix("/data", http.FileServer(http.Dir("."))))
		if err := http.ListenAndServe(":8080", nil); err != nil {
			log.Printf("Error in HTTP server: %v", err)
		}
	}()

	testOpenDatabase()
	testCreateDatabase()
	testSplitDatabase()
	testMergeDatabases()
}
