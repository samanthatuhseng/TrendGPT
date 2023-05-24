package main

import (
	"bufio"
	"context"
	"encoding/json"
	"log"
	"os"
	"io/ioutil"

	twitterscraper "github.com/n0madic/twitter-scraper"
	"github.com/tidwall/pretty"
)

type Tweet struct {
	Text string `json:"text"`
	PermanentURL string `json:"permanent_url"`
	Author string `json:"author"`
	Retweets int `json:retweets`
	Likes int `json:"likes"`
}	

type Query struct {
	Filter       string `json:"filter"`
	Explanation  string `json:"explanation"`
	// Add more properties as needed
}

func getTweets() {
	scraper := twitterscraper.New()

	err := scraper.Login("CaAr621", "CryptoArsenal!")

	file, err := os.Create("tweets.json")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	encoder := json.NewEncoder(writer)

	// Read the queries from the JSON file
	queriesFile, err := ioutil.ReadFile("queries.json")
	if err != nil {
		log.Fatal(err)
	}

	queries := []Query{}
	err = json.Unmarshal(queriesFile, &queries)
	if err != nil {
		log.Fatal(err)
	}

	tweets := []Tweet{}
	for _, query := range queries {
		for tweet := range scraper.SearchTweets(context.Background(),
			query.Filter, 50){
			if tweet.Error != nil {
				panic(tweet.Error)
			}
			t := Tweet{
						Text:         tweet.Text,
						PermanentURL: tweet.PermanentURL,
						Author: tweet.Name,
						Retweets: tweet.Retweets,
						Likes: tweet.Likes,
					}
			tweets = append(tweets, t)
		}
	}
	err = encoder.Encode(tweets)
	if err != nil {
		log.Fatal(err)
	}
	err = writer.Flush()
	if err != nil {
		log.Fatal(err)
	}

	// Read the JSON data from the file
	jsonData, err := ioutil.ReadFile("tweets.json")
	if err != nil {
		log.Fatal(err)
	}

	// Format the JSON data
	formattedJSON := pretty.Pretty(jsonData)

	// Write the formatted JSON to file or print it
	err = ioutil.WriteFile("formatted_tweets.json", formattedJSON, 0644)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	// keyword := os.Args[1]
	getTweets()
}
