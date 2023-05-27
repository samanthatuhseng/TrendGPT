import subprocess
import sys
from privateGPT import main as privateGPT

def scrape():
    command = "cd ../scraper; go build twitterscraper.go; ./twitterscraper "
    try: 
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def store():
    command = "mv ../scraper/formatted_tweets.json ../privateGPT/source_documents; python3 ingest.py"
    try: 
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def queryGPT(query):
    query, answer, docs = privateGPT(query)
    print(query, answer, docs)

def main(query: str):
    scrape()
    store()
    queryGPT(query)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cronjob.py <query>")
        sys.exit(1)
    query = sys.argv[1]
    main(query)

