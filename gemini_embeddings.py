import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"]
)

with open("resume.txt", "r") as f:
    resume_text = f.read()
    # print(resume_text)

collection.add(
    documents=[resume_text],
    ids=["resume"]
)

results = collection.query(
    query_texts=["This is a query document about hawaii"], # Chroma will embed this for you
    n_results=2 # how many results to return
)

res = collection.query(
    query_texts=['what is this persons field of study?'],
    n_results=1
)

print(res)
# print(results['documents'])