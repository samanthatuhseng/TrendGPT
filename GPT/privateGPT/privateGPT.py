from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from multiprocessing import cpu_count
from constants import CHROMA_SETTINGS

import os

load_dotenv("../privateGPT/.env")

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
model_n_batch = int(os.environ.get('MODEL_N_BATCH',8))
# Number of CPU cores
n_cpu = cpu_count()

# Now, if you want to use, say, 80% of your CPU cores:
cpu_model_n_threads = int(0.8 * n_cpu)


# embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
embeddings = OpenAIEmbeddings()

db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
retriever = db.as_retriever()
# Prepare the LLM
callbacks = [StreamingStdOutCallbackHandler()]
# set the default to 4 threads since `n_threads` defaults there.
model_n_threads = int(cpu_count() * 0.8) 

match model_type:
    case "LlamaCpp":
            llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, n_batch=model_n_batch, n_threads=model_n_threads, callbacks=callbacks, verbose=False)
    case "GPT4All":
        llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', n_batch=model_n_batch, n_threads=model_n_threads, callbacks=callbacks, verbose=False)
    case "OpenAI":
        llm = OpenAI()
    case _default:
        print(f"Model {model_type} not supported!")
        exit;

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

def main(query):
    print("querying ", query)
    # Interactive questions and answers
    # while True:
    # query = input("\nEnter a query: ")
    if query == "exit":
        return
        
    # Get the answer from the chain
    res = qa(query)    
    answer, docs = res['result'], res['source_documents']

    # Print the result
    print("\n\n> Question:")
    print(query)
    print("\n> Answer:")
    print(answer)
    
    # Print the relevant sources used for the answer
    for document in docs:
        print("\n> " + document.metadata["source"] + ":")
        print(document.page_content)

    return query, answer, docs

if __name__ == "__main__":
    main()
