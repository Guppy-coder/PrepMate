import tkinter as tk
from tkinter import messagebox
import pyaudio
import wave
import requests
import base64
from vulavula import VulavulaClient
import threading
import os
import logging
import re
import time


from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants
API_URL = "https://vulavula-services.lelapa.ai/api/v1/transcribe/sync"
VULAVULA_API_KEY = os.getenv("VULAVULA_API_KEY", "default_vulavula_key")
RECORDINGS_FOLDER = "recordings"

# Function to get the next recording file name
def get_next_recording_filename():
    # Check if the folder exists; if not, create it
    if not os.path.exists(RECORDINGS_FOLDER):
        os.makedirs(RECORDINGS_FOLDER)
        
    # List all files in the recordings folder
    files = os.listdir(RECORDINGS_FOLDER)
    
    # Filter files that match the recording pattern and extract numbers
    recording_files = [f for f in files if re.match(r'recording_(\d+)\.wav', f)]
    max_number = 0
    for file in recording_files:
        # Extract number from filename
        number = int(re.search(r'(\d+)', file).group(0))
        if number > max_number:
            max_number = number
    # Increment the highest number found by 1 for the new filename
    new_filename = f"recording_{max_number + 1}.wav"
    return new_filename

# Function to get the latest recording file path
def get_latest_recording_filepath():
    # Check if the folder exists; if not, return None
    if not os.path.exists(RECORDINGS_FOLDER):
        return None
        
    # List all files in the recordings folder
    files = os.listdir(RECORDINGS_FOLDER)
    
    # Filter files that match the recording pattern and extract numbers
    recording_files = [f for f in files if re.match(r'recording_(\d+)\.wav', f)]
    if not recording_files:
        return None
    
    # Sort files by number and get the latest one
    recording_files.sort(key=lambda f: int(re.search(r'(\d+)', f).group(0)), reverse=True)
    latest_file = recording_files[0]
    return os.path.join(RECORDINGS_FOLDER, latest_file)

# Initialize Tkinter window
root = tk.Tk()
root.title("Audio Transcription")

# Set window size and center it
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Global variables for recording
is_recording = False
audio_file = None
file_path = None
p = None
stream = None
frames = []

# Start recording functionality
def start_recording():
    global is_recording, audio_file, file_path, p, stream, frames
    if is_recording:
        messagebox.showwarning("Warning", "Recording is already in progress.")
        return

    is_recording = True
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, channels=channels, rate=rate, frames_per_buffer=chunk, input=True)
    frames = []

    def record():
        while is_recording:
            data = stream.read(chunk)
            frames.append(data)

    threading.Thread(target=record).start()
    logging.info("Recording started.")
    messagebox.showinfo("Info", "Recording started.")

# Stop recording functionality
def stop_recording():
    global is_recording, audio_file, file_path, p, stream, frames
    if not is_recording:
        messagebox.showwarning("Warning", "No recording in progress.")
        return

    is_recording = False
    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_file = get_next_recording_filename()
    file_path = os.path.join(RECORDINGS_FOLDER, audio_file)
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    logging.info(f"Recording finished. Saved as {file_path}")
    messagebox.showinfo("Info", f"Recording finished. Saved as {file_path}")

# Playback functionality
def playback_recording():
    def play():
        latest_file_path = get_latest_recording_filepath()
        if not latest_file_path:
            messagebox.showwarning("Warning", "No recordings found.")
            return

        chunk = 1024
        wf = wave.open(latest_file_path, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

        logging.info("Playback finished.")
        messagebox.showinfo("Info", "Playback finished.")

    threading.Thread(target=play).start()

# Transcription functionality
def transcribe_audio():
    client = VulavulaClient(VULAVULA_API_KEY)
    
    latest_file_path = get_latest_recording_filepath()
    if not latest_file_path:
        messagebox.showwarning("Warning", "No recordings found.")
        return

    try:
        # Submit the audio file for transcription
        upload_id, transcription_result = client.transcribe(
            latest_file_path, 
            webhook="<INSERT_URL>"
        )
        print("Transcription Submit Success:", transcription_result)

        # Polling for the transcription result
        while client.get_transcribed_text(upload_id)['message'] == "Item has not been processed.":
            time.sleep(10)
            print("Waiting for transcribe to complete...")

        # Get the transcribed text
        transcribed_text = client.get_transcribed_text(upload_id)
        print("Transcribed Text:", transcribed_text)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    logging.info("Transcription finished.")
    messagebox.showinfo("Info", "Transcription finished.")
    

# Create buttons
start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=10)

playback_button = tk.Button(root, text="Playback Recording", command=playback_recording)
playback_button.pack(pady=10)

transcribe_button = tk.Button(root, text="Transcribe Audio", command=transcribe_audio)
transcribe_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop() 