import tkinter as tk
from tkinter import filedialog
from vector_database import create_table, connect_to_db, get_vector_index_wrapper, add_data_to_vector_table, myCasandraVStore
from langchain.llms import openai
import os
from dotenv import load_dotenv

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
    
def main():
    connect_to_db()
    if myCasandraVStore is not None:
        table_name = input("insert table name: ")
        create_table(table_name)
    open_ai_api_key = os.getenv("OPENAI_API_KEY")
    upload_resume()
    llm = openai.OpenAI(open_ai_key=open_ai_api_key)
    vector_index = get_vector_index_wrapper()
    while True:
        query = "give me a summary of the users resume"
        answer = vector_index.query(query, llm=llm)
        print(answer)

main()
    