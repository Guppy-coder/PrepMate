import google.generativeai as genai
import os
import time
import speech_recognition as sr
from gtts import gTTS
import threading
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api_key)

def generate_questions():
    response = model.generate_content("You are an iterviewer. You are interviewing a candidate for a job. The candidate is a software engineer. please evalute their performance.")

    while not response.text:
        time.sleep(1)

    proficiency = "Intermediate"
    field_of_study = "Computer Science"
    type_of_interview = "Behavioral"

    print(model.generate_content("At the end give me an overall impression of the candidate's performance").text)
    

    response = model.generate_content("1. " + field_of_study + "\n2. " + type_of_interview + " Interview Questions" + "\n3. " + proficiency + " Candidate")

    questions = response.text.split("* **")

    return questions

def text_to_speech(text):
    os.system("start question.mp3")

def save_audio(text):
    tts = gTTS(text, lang='en')
    tts.save("question.mp3")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            answer = recognizer.recognize_google(audio)
            return answer
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
    
def generate_candidate_answers(questions):
    candidate_answers = {}
    count = 0
    question = questions[count]
    threading.Thread(target=save_audio, args=(question)).start()
    count += 1
    if question.startswith("**") or question.startswith("##"):
        question = questions[count + 1]
    text_to_speech(question)

    answer = speech_to_text()

    if check_if_question(answer):
        answer = answer_question(question + ": " + answer)
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
    response = make_request("based on this answer, what would be a good follow up question?: " + answer)
    return response

def evaluate_candidate():
    questions = generate_questions()
    candidate_answers = generate_candidate_answers(questions)
    follow_up_questions = {}
    for question, answer in candidate_answers.items():
        follow_up_question = generate_follow_up_question(answer)
        follow_up_questions[question] = follow_up_question
    return candidate_answers, follow_up_questions

def check_for_follow_up(answer):
    if answer is None:
        return False
    if len(answer.split()) > 20:
        response = make_request("Please generate a follow up question for this answer: " + answer)
        return response
    return False

def check_if_question(answer):
    try:    
        print("Checking if question: ", answer)
        gpt_model = genai.GenerativeModel("gemini-1.5-flash")
        response = gpt_model.generate_content("Is this a question? answer yes or no: " + answer)
        if response.text == "Yes. \n" or response.text == "Yes \n":
            print(response)
            return True
        return False
    except Exception as e:
        print(e)
        return False

def answer_question(answer):
    return make_request(answer)

def make_request(request):
    response = model.generate_content(request)
    return response.text