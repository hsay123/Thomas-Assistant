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
newsapi = "ebca6ac8613945fc8d923a63c8332e5c"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize the mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the music
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Check if the music is playing
        pygame.time.Clock().tick(10)  # Wait a bit

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return "AI not configured. Set OPENAI_API_KEY."
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Thomas. Keep responses short."},
            {"role": "user", "content": command},
        ],
    )

    return completion.choices[0].message.content

def processCommand(c): 
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()

        ## to extract the headlines
        articles = data.get('articles', [])

        ## to speak the headlines
        for article in articles:
            speak(article['title'])

    else:
        # Let the OpenAi handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Thomas.....")
    while True:
        # recognize/ listen and wake to the word Whistle
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("listening....")
                audio = r.listen(source, timeout= 3, phrase_time_limit=2)
            word= r.recognize_google(audio)
            if(word.lower() ==  "thomas"):
                speak("Ya")
                #listen for command
                with sr.Microphone() as source:
                    print("Thomas is active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e)) 