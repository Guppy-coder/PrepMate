import chromadb
import openai
import os
import pprint
import pandas as pd
from transformers import pipeline

import kagglehub

# Download latest version
path = kagglehub.dataset_download("syedmharis/software-engineering-interview-questions-dataset")

print("Path to dataset files:", path)




chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="my_collection")

with open("resume.txt", "r") as f:
    resume_text = f.read()
    # print(resume_text)

collection.add(
    documents=[resume_text],
    ids=["resume"]
)

res = collection.query(
    query_texts=['what is this persons field of study?'],
    n_results=1
)

# Extract the relevant document from the query results
relevant_document = res['documents'][0]



pprint(resp)