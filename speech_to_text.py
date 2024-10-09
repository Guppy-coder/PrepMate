import speech_recognition as sr

while True:

    try:
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)
            answer = recognizer.recognize_google(audio)
            print(answer)

    except sr.UnknownValueError:
        print("Could not understand audio")
        recognizer.listen(mic)
        continue
