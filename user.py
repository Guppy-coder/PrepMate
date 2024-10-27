import tkinter as tk
from tkinter import filedialog
from vector_database import create_table, connect_to_db, get_vector_index_wrapper, add_data_to_vector_table, VStore
from langchain.llms import openai
import os
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

load_dotenv()

open_ai_api_key = os.getenv("OPENAI_API_KEY")

def upload_resume():

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Resume",
        filetypes=(("pdf files", "*.pdf"),("Word file", "*.docx"), ("All files", "*.*"))
    )

    if file_path:
        with open(file_path, "rb") as f:
            content = f.read()
            print(content)
            try:
                table = get_vector_index_wrapper()
                add_data_to_vector_table(table, content)
            except Exception:
                print("could not upload contents of file")
        return content
    else:
        return None

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def query_vector_index(query, vector_index, llm):
    return vector_index.query(query, llm=llm)

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def create_my_cassandra_vstore(table_name):
    return create_table(table_name)

def main():
    if VStore is None:
        table_name = input("insert table name: ")
        try:
            create_my_cassandra_vstore(table_name)
        except openai.error.RateLimitError:
            print("Rate limit error")
            return
    open_ai_api_key = os.getenv("OPENAI_API_KEY")
    upload_resume()
    llm = openai.OpenAI(open_ai_api_key)
    vector_index = get_vector_index_wrapper()
    while True:
        query = "give me a summary of the users resume"
        try:
            answer = query_vector_index(query, vector_index, llm)
            print(answer)
        except openai.error.RateLimitError:
            print("Rate limit error")
            break

main()
    