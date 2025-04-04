package main

import (
	"fmt"
	"log"
	"mapreduce"
)

func main() {
	// open austen.db
	db, err := mapreduce.OpenDatabase("austen.db")
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer db.Close()

	// a query to count rows in the "pairs" table
	var count int
	err = db.QueryRow("select count(1) from pairs").Scan(&count)
	if err != nil {
		log.Fatalf("Query error: %v", err)
	}
	fmt.Printf("The austen.db contains %d rows in the pairs table.\n", count)
}
