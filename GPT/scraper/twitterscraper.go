package main

import (
	"bufio"
    "context"
    "fmt"
	"log"
	"os"
    twitterscraper "github.com/n0madic/twitter-scraper"
)

func getTweets(keyword string) {
    scraper := twitterscraper.New()

	// Open a file for writing
	file, err := os.Create("tweets.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Create a writer to write to the file
	writer := bufio.NewWriter(file)


    for tweet := range scraper.GetTweets(context.Background(), keyword, 50) {
        if tweet.Error != nil {
            panic(tweet.Error)
        }
        // Write the tweet text to the file
		_, err := writer.WriteString(tweet.Text + "\n")
		if err != nil {
			log.Fatal(err)
		}
    }
	// Flush the writer to ensure all data is written to the file
	err = writer.Flush()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tweets saved to tweets.txt")
}

func main() {
	keyword := os.Args[1]
	getTweets(keyword)
}

