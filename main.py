import speech_recognition
import pyttsx3

import tools.logging as logger

import datetime
import random

import config as cfg

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[cfg.voice_index].id)

# LISTEN
def mic_input():
    try:
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            print("Listening...")
            recognizer.energy_threshold = 4000
            audio = recognizer.listen(source, timeout=30, phrase_time_limit=20)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in').lower()
            print(f"User said: {command}\n")

        except Exception:
            print("Say that again please...")
            command = mic_input()
        
        logger.log_request(command, "info")
        return command
    
    except Exception as e:
        print(e)
        return False

# SPEAK
def text_to_speech(text):
    try:
        engine.say(text)
        engine.runAndWait()
        engine.setProperty('rate', 175)
        return True
    
    except Exception as ex:
        logger.log_error("Error in text_to_speech function: " + ex)
        return False



def speak(text):
    text_to_speech(text)
    logger.log_response(text, "info", cfg.RESPONSE_TYPE)


def startup():
    speak("Initializing JARVIS")
    speak("Importing preferences and calibrating virtual environment")
    speak("JARVIS online and ready")
    greeting()


def greeting():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

    speak(f"It is {datetime.time()}")
    speak("How can I help you today?")
    logger.log_info("Startup complete")