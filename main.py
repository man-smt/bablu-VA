import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your Key Here>"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# def aiProcess(command):
#     client = OpenAI(api_key="<Your Key Here>")
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a virtual assistant named bablu skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
#             {"role": "user", "content": command}
#         ]
#     )
#     return completion.choices[0].message.content

def processCommand(c):
    print(c.lower())
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        parts = c.lower().split(" ", 1)
        if len(parts) > 1:
            song = parts[1]
            if song in musicLibrary.music:
                link = musicLibrary.music[song]
                webbrowser.open(link)
            else:
                print("called")
                # fallback: search on YouTube
                search_url = f"https://www.youtube.com/results?search_query={song}"
                webbrowser.open(search_url)
                speak(f"I couldn't find {song} in my library, searching on YouTube.")
        else:
            speak("Please tell me what to play.")

    # elif "news" in c.lower():
    #     r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    #     if r.status_code == 200:
    #         data = r.json()
    #         articles = data.get('articles', [])
    #         for article in articles:
    #             speak(article['title'])
    # else:
    #     output = aiProcess(c)
    #     speak(output)

# --- Microphone setup ---
def get_microphone():
    print("Available microphones:")
    for i, mic in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i}: {mic}")
    # pick first device by default
    return sr.Microphone(device_index=0)

if __name__ == "__main__":
    speak("Initializing bablu....")
    mic = get_microphone()
    while True:
        r = sr.Recognizer()
        # print("recognizing...")
        try:
            with mic as source:
                # print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=2)
            word = r.recognize_google(audio)
            print(word)
            if "bablu" in word.lower():
                speak("yes friend!")
                with mic as source:
                    print("bablu Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            # print("Error:", e)
            pass
