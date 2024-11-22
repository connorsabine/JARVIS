import speech_recognition as sr
import pyttsx3
import sys
import time
import jarvis.config as config


engine = pyttsx3.init()
engine.setProperty('rate', config.SPEED)
engine.setProperty('volume', config.VOLUME)


def startup():
    speak(f"Hello {config.ADDRESS}, i'm JARVIS. How can I assist you today?")


def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()


def mic_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)

    try:
        command = recognizer.recognize_google(audio, language='en-in').lower()
        print(f"USER: {command}")
        return command
    
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please repeat.")
        return mic_input()
    
    except sr.RequestError as e:
        speak("Sorry, I'm having trouble reaching the speech service.")
        print(f"Error: {e}")
        return None


def terminal_input():
    command = input("Enter your command: ").lower()
    return command


def switch_to_terminal_mode():
    config.INTERACTION_TYPE = "Terminal"
    speak("Switching to terminal mode.")


def switch_to_voice_mode():
    config.INTERACTION_TYPE = "Voice"
    speak("Switching to voice mode.")