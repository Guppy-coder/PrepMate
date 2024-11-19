from pinecone import Pinecone
import os
from pinecone_plugins.assistant.models.chat import Message
import tkinter as tk
from tkinter import filedialog
import functools
# import magic
import docx2pdf


# msg = Message(content="How many employees did Netflix have by the end of 2023?")
# resp = assistant.chat(messages=[msg])

# print(resp['message']['content'])
is_assistant_created = False
assistant_name = ""
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def get_input(prompt):
    is_valid_input = False

    while not is_valid_input:
        user_input = input(prompt)
        if user_input == None:
            continue
        else:
            is_valid_input = True
    
    return user_input.strip()

def upload_CV(assistant):
    file_path = filedialog.askopenfilename()
    # Do something with the file path, like uploading it to a server or processing it locally
    # if not is_pdf:
    #     docx2pdf.convert("input.docx", "output.pdf")
    assistant.upload_file(file_path=file_path, timeout=None)
    return file_path

def get_assistant():
    assistant = pc.assistant.Assistant(
        assistant_name=assistant_name + "-assistant", 
    )

    return assistant

# def is_pdf(file_path):
#     mime_type = magic.from_file(file_path, mime=True)
#     return mime_type == 'application/pdf'

def main():

    global assistant_name
    
    assistant_name = get_input("Name your assistant: ")
    

    global is_assistant_created
    if not is_assistant_created:
        try:
            assistant = pc.assistant.create_assistant(
                assistant_name= assistant_name + "-assistant", 
                instructions="", # Description or directive for the assistant to apply to all responses.
                timeout=30 # Wait 30 seconds for assistant operation to complete.
        )
        except Exception:
            print("Assistant already exists")
            is_assistant_created = True


if __name__ == "__main__":
    main()

root = tk.Tk()
root.title("File Uploader")

assistant = get_assistant()

upload_with_args = functools.partial(upload_CV, assistant)

upload_button = tk.Button(root, text="Upload File", command=upload_with_args)
upload_button.pack()

root.mainloop()