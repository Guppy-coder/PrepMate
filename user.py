import tkinter as tk
from tkinter import filedialog

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
        return content
    else:
        return None