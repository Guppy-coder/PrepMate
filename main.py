import time
from API import evaluate_candidate

def main(): 
    start_time = time.time()
    time_limit = 600
    while time.time() - start_time < time_limit:
        candidate_answers, follow_up_questions = evaluate_candidate()
        print("Candidate Answers: ", candidate_answers)
        print("Follow Up Questions: ", follow_up_questions)

if __name__ == "__main__":
    main()