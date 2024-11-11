import pandas as pd
import chromadb
from pprint import pprint

# Load the data
questions_df = pd.read_csv('Software Questions.csv')

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="questions_collection")

ids = [f'field_{i}' for i in range(len(questions_df))]

collection.add(
    documents=questions_df['questions'].tolist(),
    ids=ids
)

res = collection.query(
    query_texts=['skills', 'programming', 'languages'],
    n_results=5
)

pprint(res)