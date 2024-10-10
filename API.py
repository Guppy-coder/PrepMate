import google.generativeai as genai
import os
import time
import speech_recognition as sr
from gtts import gTTS


api_key = os.getenv('GENAI_API_KEY')
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_questions():
    response = model.generate_content("You are an iterviewer. You are interviewing a candidate for a job. The candidate is a software engineer. please evalute their performance.")

    while not response.text:
        time.sleep(1)

    proficiency = "Intermediate"
    field_of_study = "Computer Science"
    type_of_interview = "Behavioral"

    model.generate_content("At the end give me an overall impression of the candidate's performance")

    response = model.generate_content("1. " + field_of_study + "\n2. " + type_of_interview + " Interview Questions" + "\n3. " + proficiency + " Candidate")

    questions = response.text.split("* **")

    return questions

def text_to_speech(text):
    tts = gTTS(text, lang='en')
    tts.save("question.mp3")
    os.system("start question.mp3")

def speech_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    try:
        print("Listening...")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            answer = recognizer.recognize_google(audio)
            return answer
    except sr.UnknownValueError:
        print("Could not understand audio")
        recognizer.listen(source)
    
def generate_candidate_answers(questions):
    candidate_answers = {}
    for question in questions:
        if question.startswith("**") or question.startswith("##"):
            continue
        text_to_speech(question)
        time.sleep(20)
        answer = speech_to_text()

        if check_if_question(answer):
            answer = answer_question(answer)
            text_to_speech(answer)

        if check_for_follow_up(answer):
            follow_up_question = generate_follow_up_question(answer)
            text_to_speech(follow_up_question)
            time.sleep(20)
            follow_up_answer = speech_to_text()
            candidate_answers[question] = (answer, follow_up_answer)
        candidate_answers[question] = answer
    return candidate_answers

def evaluate_candidate():
    questions = generate_questions()
    candidate_answers = generate_candidate_answers(questions)
    return candidate_answers

def generate_follow_up_question(answer):
    print("Generating follow up question for: ", answer)
    response = model.generate_content("based on this answer, what would be a good follow up question?: " + answer)
    return response.text

def evaluate_candidate():
    questions = generate_questions()
    candidate_answers = generate_candidate_answers(questions)
    follow_up_questions = {}
    for question, answer in candidate_answers.items():
        follow_up_question = generate_follow_up_question(answer)
        follow_up_questions[question] = follow_up_question
    return candidate_answers, follow_up_questions

def check_for_follow_up(answer):
    if len(answer.split()) > 20:
        response = model.generate_content("Please generate a follow up question for this answer: " + answer)
        return response.text
    return False

def check_if_question(answer):
    print("Checking if question: ", answer)
    response = model.generate_content("Is this a question? answer yes or no: " + answer)
    if response.text.lower() == "yes":
        return True
    return False

def answer_question(answer):
    response = model.generate_content("Answer the question: " + answer)
    return response.text