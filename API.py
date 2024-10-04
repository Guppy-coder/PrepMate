import google.generativeai as genai
import os
import time
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment


api_key = os.getenv('GENAI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")

genai.configure(api_key=os.environ['GENAI_API_KEY'])
 
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("You are an iterviewer. You are interviewing a candidate for a job. The candidate is a software engineer. please evalute their performance.")
# print(response.text)

while not response.text:
    time.sleep(1)

proficiency = "Intermediate"
field_of_study = "Computer Science"
type_of_interview = "Behavioral"

model.generate_content("At the end give me an overall impression of the candidate's performance")

response = model.generate_content("1. " + field_of_study + "\n2. " + type_of_interview + " Interview Questions" + "\n3. " + proficiency + " Candidate")
print(response.text)

questions = response.text.split("* **")
# print(questions)

candidate_answers = {}

for question in questions:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    if question.startswith("**") or question.startswith("##"):
        continue
    with mic as source:
        # print(question)
        tts = gTTS(question, lang='en')
        tts.save("question.mp3")
        os.system("mpg123 question.mp3")

        audio_file = AudioSegment.from_file("/home/wethinkcode_/student_work/personal_prodj/PrepMate-1/question.mp3")
        audio_duration = len(audio_file) / 1000
        try:
            # time.sleep(audio_duration)
            print("Listening...")
            audio = recognizer.listen(source)
            answer = recognizer.recognize_google(audio)
            candidate_answers[question] = answer
            print(candidate_answers) 
        except sr.UnknownValueError:
            comp = "Sorry, I did not get that"
            tts = gTTS(comp, lang='en')
            tts.save("comp.mp3")
            os.system("mpg123 comp.mp3")
            print(candidate_answers) 

print(candidate_answers)