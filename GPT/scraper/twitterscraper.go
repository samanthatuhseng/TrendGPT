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

	query := `(crypto OR cryptocurrency OR bitcoin OR ethereum OR btc OR eth OR blockchain) (from:elonmusk OR from:VitalikButerin OR from:SatoshiLite OR from:brian_armstrong OR from:cz_binance OR filter:verified) -filter:retweets :) OR :( OR ?`

	tweets := []Tweet{}
	for tweet := range scraper.SearchTweets(context.Background(),
        query, 50){
		if tweet.Error != nil {
			panic(tweet.Error)
		}

		t := Tweet{
			Text:         tweet.Text,
			PermanentURL: tweet.PermanentURL,
			Author: tweet.Name,
			Retweets: tweet.Retweets,
			Likes: tweet.Likes,
			// Set additional fields as needed
		}

		tweets = append(tweets, t)
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
