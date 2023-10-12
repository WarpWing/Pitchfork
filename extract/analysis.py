import openai
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, StorageContext, VectorStoreIndex, ServiceContext, set_global_service_context
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()
openai.api_key = ""

def construct_index(directory_path):
    documents = SimpleDirectoryReader(directory_path,recursive=True).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir="./storage")
    return index

def query(index, input_text):
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response

directory_path = "./storage"
index = construct_index(directory_path)
print(query(index, "Give me a Json file for the Breakfast menu for Monday and thats it. Be specific and check the files."))