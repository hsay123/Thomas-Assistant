import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import pywhatkit

# Initialize text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# News API setup (replace with your API key)
NEWS_API_KEY = "ebca6ac8613945fc8d923a63c8332e5c"
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to your voice command
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the internet.")
            return ""

# Function to fetch and read news
def get_news():
    response = requests.get(NEWS_URL)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data["articles"][:5]  # Get top 5 headlines
        speak("Here are the latest news headlines.")
        for i, article in enumerate(articles, 1):
            headline = article["title"]
            speak(f"News {i}: {headline}")
            # Check for "stop" command while reading news
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                try:
                    interrupt = recognizer.recognize_google(audio).lower()
                    if "stop" in interrupt:
                        speak("Stopping the news.")
                        return
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    continue
    else:
        speak("Sorry, I couldn't fetch the news right now.")

# Main loop for the voice assistant
def voice_assistant():
    speak("Hello! I'm your voice assistant. How can I help you?")
    while True:
        command = listen()

        # Exit condition
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        # Open websites
        elif "open" in command:
            if "google" in command:
                speak("Opening Google.")
                webbrowser.open("https://www.google.com")
            elif "youtube" in command or "you tube" in command:
                speak("Opening YouTube.")
                webbrowser.open("https://www.youtube.com")
            elif "instagram" in command:
                speak("Opening Instagram.")
                webbrowser.open("https://www.instagram.com")
            elif "facebook" in command:
                speak("Opening Facebook.")
                webbrowser.open("https://www.facebook.com")
            else:
                speak("I can only open Google, YouTube, Instagram, or Facebook. Please try again.")

        # Play songs on YouTube
        elif "play" in command:
            song = command.replace("play", "").strip()
            if song:
                speak(f"Playing {song} on YouTube.")
                pywhatkit.playonyt(song)
            else:
                speak("Please tell me the name of the song to play.")

        # Fetch and read news
        elif "news" in command:
            speak("Fetching the news for you.")
            get_news()

        # Fallback for unrecognized commands
        elif command:
            speak("I didn't understand that. You can say 'open Google,' 'play a song,' or ask for news.")

# Run the assistant
if __name__ == "__main__":
    voice_assistant()