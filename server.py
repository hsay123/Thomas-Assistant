from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import webbrowser
import requests
from typing import Optional, Literal, Dict, Any
import os

# Optional OpenAI import; only used if key is present
try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

class CommandRequest(BaseModel):
    command: str

class ActionResponse(BaseModel):
    action: Literal[
        "speak", "open_url", "play_song", "news", "ai_reply", "error"
    ]
    message: str
    data: Optional[Dict[str, Any]] = None

app = FastAPI(title="Thomas Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


def ai_process(command: str) -> str:
    if not OPENAI_API_KEY or OpenAI is None:
        return "AI is not configured. Please set OPENAI_API_KEY."
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Thomas. Keep responses short.",
            },
            {"role": "user", "content": command},
        ],
    )
    return completion.choices[0].message.content or ""


def fetch_news_titles(limit: int = 5):
    if not NEWS_API_KEY:
        return [
            "News API key is not set. Provide NEWS_API_KEY to enable headlines.",
        ]
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return [f"Failed to fetch news. Status code: {resp.status_code}"]
        data = resp.json()
        articles = data.get("articles", [])
        titles = [a.get("title", "Untitled") for a in articles[:limit]]
        if not titles:
            return ["No news articles available right now."]
        return titles
    except Exception:
        return ["Could not fetch news at the moment."]


@app.post("/process", response_model=ActionResponse)
def process(cmd: CommandRequest):
    c = cmd.command.strip().lower()
    if not c:
        return ActionResponse(action="error", message="Empty command")

    # Open websites
    if c.startswith("open "):
        if "google" in c:
            return ActionResponse(action="open_url", message="Opening Google", data={"url": "https://google.com"})
        if "youtube" in c or "you tube" in c:
            return ActionResponse(action="open_url", message="Opening YouTube", data={"url": "https://youtube.com"})
        if "instagram" in c:
            return ActionResponse(action="open_url", message="Opening Instagram", data={"url": "https://instagram.com"})
        if "facebook" in c:
            return ActionResponse(action="open_url", message="Opening Facebook", data={"url": "https://facebook.com"})
        if "linkedin" in c:
            return ActionResponse(action="open_url", message="Opening LinkedIn", data={"url": "https://linkedin.com"})
        if "chatgpt" in c:
            return ActionResponse(action="open_url", message="Opening ChatGPT", data={"url": "https://chatgpt.com"})
        return ActionResponse(action="speak", message="I can open Google, YouTube, Instagram, Facebook, LinkedIn, or ChatGPT.")

    # Play a song on YouTube
    if c.startswith("play "):
        song = c.replace("play", "", 1).strip()
        if song:
            # Frontend can open this search link
            return ActionResponse(
                action="play_song",
                message=f"Playing {song} on YouTube",
                data={"url": f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"},
            )
        return ActionResponse(action="speak", message="Please tell me the name of the song.")

    # News
    if "news" in c:
        titles = fetch_news_titles(limit=5)
        return ActionResponse(action="news", message="Here are the latest headlines:", data={"titles": titles})

    # Fallback to AI
    reply = ai_process(cmd.command)
    return ActionResponse(action="ai_reply", message=reply)


# For uvicorn: uvicorn server:app --host 0.0.0.0 --port 8000

