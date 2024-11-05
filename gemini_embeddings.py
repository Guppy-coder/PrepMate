import chromadb
import os
import pprint
from dotenv import load_dotenv
import google.generativeai as genai
from time import sleep

import kagglehub


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


# initialize gemini client

# Download latest version
# path = kagglehub.dataset_download("syedmharis/software-engineering-interview-questions-dataset")

# print("Path to dataset files:", path)




chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="my_collection")

with open("resume.txt", "r") as f:
    resume_text = f.read()
    fields = resume_text.split("\n")
    # print(resume_text)

ids = [f'field_{i}' for i in range(len(fields))]

print(len(fields))

collection.add(
    documents=fields,
    ids=ids
)

res = collection.query(
    query_texts=['skills', 'programming', 'languages'],
    n_results=5
)

skills = res['documents'][0]
programming = res['documents'][1]

# pprint.pprint(res)
behavioral_template = """ I want you to act as an interviewer. Remember, you are the interviewer not the candidate.   
            Let's think step by step.
            
            Based on the keywords, 
            Create a guideline with the following topics for a behavioral interview to test the soft skills of the candidate. 
            
            Do not ask the same question.
            Do not repeat the question. 
            
            Keywords: 
            {context}
       
            Question: {question}
            Answer:"""

res = model.generate_content(behavioral_template)

pprint.pprint(res)

questions = res.text.split("* **")
print(len(res))
questions = questions[0].split("\n")
print(len(questions))

pprint.pprint(questions)

for ques in questions:
    if ques == "":
        continue
    print(ques)
    print()
    sleep(2)
