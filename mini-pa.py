from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import json
import tkinter as tk
from tkinter import filedialog

from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores.cassandra import Cassandra
from datasets import load_dataset
from tenacity import retry, wait_exponential, stop_after_attempt
from langchain_community.llms import openai

from dotenv import load_dotenv
import os

load_dotenv()
OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')

with open("tsgsekgothe6969@gmail.com-token.json") as f:
        secrets = json.load(f)

ASTRA_DB_CLIENT_ID = secrets["clientId"]
ASTRA_DB_CLIENT_SECRET = secrets["secret"]

ASTRA_DB_SECURE_BUNDLE_PATH = "secure-connect-prep-mate-db.zip"
ASTRA_DB_APPLICATION_TOKEN = secrets["token"]
ASTRA_DB_KEYSPACE = "prep_mate"

cloud_config= {
    'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
}
auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

llm = openai.OpenAI(openai_api_key=OPEN_AI_KEY)
myembeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_KEY)

def upload_resume():

    # root = tk.Tk()
    # root.withdraw()

    # file_path = filedialog.askopenfilename(
    #     title="Select Resume",
    #     filetypes=(("pdf files", "*.pdf"),("Word file", "*.docx"), ("All files", "*.*"))
    # )

    # if file_path:
    with open("resume.txt", "rb") as f:
        content = f.read()
    return content
    # else:
    #     return None
    
def create_table(table_name):
    myCasandraVStore=Cassandra(
        embedding=myembeddings,
        session=session,
        keyspace=ASTRA_DB_KEYSPACE,
        table_name=table_name
    )

    return myCasandraVStore


def main():
    table_name = input("insert table name: ")
    try:
        myCasandraVStore = create_table(table_name)
    except openai.error.RateLimitError:
        print("Rate limit error")
        return
    upload_resume()
    vector_index = VectorStoreIndexWrapper(myCasandraVStore)
    while True:
        query = "give me a summary of the users resume"
        answer = vector_index.query(query, llm=llm)
        print(answer)

if __name__ == "__main__":
    main()