import google.generativeai as genai
import os
import time
import speech_recognition as sr


api_key = os.getenv('GENAI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")

genai.configure(api_key=os.environ['GENAI_API_KEY'])
 
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("You are an iterviewer. You are interviewing a candidate for a job. The candidate is a software engineer. please evalute their performance.")
print(response.text)

while not response.text:
    time.sleep(1)

recognizer = sr.Recognizer()
microphone = sr.Microphone()
with  microphone as source:
    print("Please say how proficient are you? ")
    audio = recognizer.listen(source)
    proficiency = recognizer.recognize_google(audio)
    print(proficiency)

    print("Please state your field of study")
    audio = recognizer.listen(source)
    field_of_study = recognizer.recognize_google(audio)
    print(field_of_study)

    print("Please state the type of interview")
    audio = recognizer.listen(source)
    type_of_interview = recognizer.recognize_google(audio)
    print(type_of_interview)

model.generate_content("At the end give me an overall impression of the candidate's performance")


response = model.generate_content("1. " + field_of_study + "\n2. " + type_of_interview + " Interview Questions" + "\n3. " + proficiency + " Candidate")
# print(response.text)
list = response.text.split("\n")
General_concepts = []
for i in list[3:]:
    print(i)
    ques = i.split("\n")
    General_concepts.append(ques)

print(General_concepts)