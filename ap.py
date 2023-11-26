import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import random
import os
import smtplib
from pydub import AudioSegment
from pydub.playback import play
# from moviepy.editor import *
import pygame
from pydub.playback import play
from gtts import gTTS


# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def sendEmail(to, subject, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('spoorthyuk2000@gmail.com', 'rlllsahcdqetxhyv')

        message = f"Subject: {subject}\n\n{content}"
        server.sendmail('spoorthyuk2000@gmail.com', to, message)

        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", str(e))


# Initialize pygame
pygame.init()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio, talking_video=False):
    engine.say(audio)
    engine.runAndWait()


def text_to_speech(text, output_filename):
    engine.save_to_file(text, output_filename)
    engine.runAndWait()
    return output_filename

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 100
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if any(greeting in query.lower() for greeting in greetings):
            return "greeting"
    
    except Exception as e:
        print("Say that again please...")
        return "None"

    return query

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I'm your voice assistant . How can I assist you today?")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except Exception as e:
        return "Sorry, I couldn't find any relevant information."
    
def get_date():
    today = datetime.datetime.now()
    date_str = today.strftime("%B %d, %Y")
    return date_str

def get_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    return time_str

def respond_to_greeting():
    greetings = [
        "Hi there! How can I assist you today?",
        "Hello! How can I help you?",
        "Hey! What can I do for you?",
        "Good day! How can I be of service?",
    ]
    greeting = random.choice(greetings)
    speak(greeting)


# Your existing functions for sendEmail, alphabetss, ludo...

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if query == "greeting":
            respond_to_greeting()
        
        elif "date" in query:
            date = get_date()
            speak(f"Today's date is {date}")

        elif "time" in query:
            time = get_time()
            speak(f"The current time is {time}")
    
        elif 'send email' in query:
            try:
                speak("To whom should I send the email?")
                to = takeCommand().lower().replace(" ", "") + "@gmail.com"

                speak("What is the subject of the email?")
                subject = takeCommand()

                speak("What should I say in the email?")
                content = takeCommand()

                sendEmail(to, subject, content)
                speak("Email has been sent!")

            except Exception as e:
                speak("Sorry, I could not send the email. Please try again.")
        
        elif 'wikipedia'in query:
            try:
                speak('Searching Wikipedia...')
                results = wikipedia.summary(query, sentences=2)
                print(results)
                speak(results)
            except Exception as e:
                print('There is no such content here!')
                speak('No result found')


        elif 'open website' in query:
            try:
                # Website opening logic
                speak("Which website should I open?")
                website = takeCommand().lower().replace(" ", "")
                webbrowser.open(f"https://{website}.com")
                speak(f"Opening {website}.com")

            except Exception as e:
                speak("Sorry, I couldn't open the website.")

        elif 'tell me a joke' in query:
            # Jokes list for random selection
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Parallel lines have so much in common. It's a shame they'll never meet.",
                "I told my wife she was drawing her eyebrows too high. She seemed surprised.",
                "Why don't skeletons fight each other? They don't have the guts.",
                "I used to play piano by ear, but now I use my hands.",
            ]
            joke = random.choice(jokes)
            speak(joke)

        elif 'exit' in query or 'bye' in query or 'goodbye' in query:
            speak("Goodbye! Have a great day!")
            break
