import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "ebca6ac8613945fc8d923a63c8332e5c"

def speak(text):
    engine.say(text)
    engine.runAndWait()


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
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()

                # Extract headlines
                articles = data.get('articles', [])

                # Check if articles are available
                if articles:
                    speak("Here are the top news headlines. Say 'stop' to end.")
                    for article in articles[:5]:  # Limit to the first 5 headlines
                        speak(article['title'])
                        
                        # Listen for "stop" command
                        with sr.Microphone() as source:
                            try:
                                print("Listening for 'stop'...")
                                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                                command = recognizer.recognize_google(audio).lower()
                                if "stop" in command:
                                    speak("Stopping news updates.")
                                    break
                            except sr.WaitTimeoutError:
                                continue  # Continue if no input is detected
                            except sr.UnknownValueError:
                                continue  # Continue if speech is not recognized
                else:
                    speak("No news articles are available right now.")
            else:
                speak(f"Failed to fetch the news. Status code: {r.status_code}")
        except requests.exceptions.RequestException as e:
            speak("I couldn't fetch the news at the moment.")
            print(f"Error fetching news: {e}")

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
                audio = r.listen(source, timeout= 5, phrase_time_limit=3)
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