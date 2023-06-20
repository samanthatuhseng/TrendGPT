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
    #command = "mv ../scraper/formatted_tweets.json ../privateGPT/source_documents; python3 ingest.py"
    command = "cd ../privateGPT; python3 ingest.py"
    try: 
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def queryGPT(query):
    # scrape()
    # store()
    query, answer, docs = privateGPT(query)
    serialized_docs = [doc.dict() for doc in docs]
    result = {
        "query": query,
        "answer": answer,
        "docs": serialized_docs
    }
    return result

def main():
    scrape()
    store()
    # queryGPT(query)

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 2:
        print("Usage: python3 cronjob.py <query>")
        sys.exit(1)
    command = sys.argv[1] # load, query
    if command == 'load': # cronjob.py load 
        print("loading")
        main()
    elif command == 'query': # cronjob.py query "query"
        print("querying")
        query = sys.argv[2]
        queryGPT(query)
    else:
        print("should be query or load")
