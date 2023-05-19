import subprocess
## function 1
## input: what to scrape for twitter scraper
## output: store it as txt file, move it to the source documents and have it ingested by the privateGPT
## function 2
## input: takes in a txt file => move the txt file to source_documents => ingest it by the private GPT
## function 3
## input: a question/query 
# output: answer from privateGPT

def scrape(keyword):
    command = "cd GPT/scraper; go build twitterscraper.go; ./twitterscraper " + keyword
    try: 
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def store():
    command = "mv GPT/scraper/tweets.txt GPT/privateGPT/source_documents; cd GPT/privateGPT; python ingest.py"
    try: 
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def run_command_with_input(command, input_str):
    try:
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output, _ = process.communicate(input_str)  # Send input to the process
        exit_code = process.returncode  # Get the command's exit code
        return exit_code, output.strip()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# def handle_user_query():
#     query = input("Enter your query: ")
#     return query

def queryGPT(query):
    command = "cd GPT/privateGPT && python privateGPT.py"
    exit_code, output = run_command_with_input(command, query)
    # if exit_code == 0:
    #     print("Command completed successfully.")
    #     handle_user_query()
    # else:
    #     print("Command failed.")


# def queryGPT(query):
#     command = f"cd GPT/privateGPT; python privateGPT.py '{query}';"   
#     try: 
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         print(result)
#         subprocess.run("exit()", shell=True, capture_output=True, text=True)
#         # callback(result)
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

# def handleCallback(query, results):
#     result = subprocess.run(query, shell=True, capture_output=True, text=True)
# scrape("soccer")
# store()
queryGPT("who is messi")

