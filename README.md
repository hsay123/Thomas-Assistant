# 🎙️ Thomas Voice Assistant

A voice-powered AI assistant with both a **web frontend** (FastAPI + browser) and a **desktop microphone mode** (Python). Thomas listens for your commands and can open websites, fetch news, play music on YouTube, and answer anything via GPT-4o-mini.

---

## Architecture

```
┌─────────────────────────────────┐     ┌──────────────────────────────────────┐
│         Frontend (web/)         │     │        Backend (FastAPI server.py)   │
│                                 │     │                                      │
│  index.html ──► script.js       │     │  FastAPI App ──► Command Router      │
│       │              │          │     │                        │              │
│  Mic/Text Input  Web Speech API │     │          ┌─────────────┴───────────┐  │
│                       │         │     │          ▼                         ▼  │
│                       └─────────┼────►│   GET /health          POST /process  │
│                    HTTP POST    │     │                              │         │
└─────────────────────────────────┘     └──────────────────────────────────────┘
                                                           │
              ┌────────────────────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                        │
│                                                             │
│  OpenAI GPT-4o-mini │ NewsAPI │ YouTube/URLs │ musicLibrary │
└─────────────────────────────────────────────────────────────┘

 Legacy desktop mode (main.py): pyttsx3 / gTTS + pygame + SpeechRecognition
```

### How it works

**Web mode** — The browser captures voice via the Web Speech API or accepts typed text, then sends a `POST /process` request to the FastAPI backend. The backend parses the command and returns a structured `ActionResponse` (`speak`, `open_url`, `play_song`, `news`, `ai_reply`, or `error`). The frontend handles the response — opening URLs, reading out text, or displaying headlines.

**Desktop mode** — `main.py` uses `speech_recognition` to listen on the microphone, waits for the wake word **"Thomas"**, then processes the command locally using the same routing logic and speaks the reply via `gTTS` + `pygame`.

---

## Project Structure

```
Thomas-Assistant/
├── server.py          # FastAPI backend — all API endpoints & command routing
├── main.py            # Desktop microphone mode (wake-word: "Thomas")
├── main2.py / main3.py # Experimental iterations
├── client.py          # Standalone Python client
├── musicLibrary.py    # Song name → YouTube URL mapping
├── requirements.txt   # Python dependencies
├── web/
│   ├── index.html     # Frontend UI
│   └── script.js      # Browser logic (speech recognition + API calls)
└── .gitignore
```


<div align="center">
  <img src="Screenshot From 2026-03-24 23-41-35.png" width="800" alt="System Architecture" style="border-radius:10px; />
</div>

    
```

## Supported Commands

| Command | Action |
|---|---|
| `open google / youtube / instagram / facebook / linkedin / chatgpt` | Opens the website in a new tab |
| `play <song name>` | Searches YouTube for the song |
| `news` | Fetches and reads top US headlines via NewsAPI |
| Anything else | Forwarded to GPT-4o-mini for a natural language response |

---

## Setup

### Backend

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API keys
export OPENAI_API_KEY=your_openai_key   # required for AI replies
export NEWS_API_KEY=your_newsapi_key    # required for news headlines

# 4. Start the server
uvicorn server:app --host 0.0.0.0 --port 8000
```

Health check: `GET http://localhost:8000/health`

### Frontend

```bash
cd web
python3 -m http.server 5050
# then open http://localhost:5050
```

Or just open `web/index.html` directly in any browser. If the backend isn't on `localhost:8000`, update the URL in `web/script.js`.

### Desktop (microphone) mode

```bash
python3 main.py
# Say "Thomas" to activate, then speak your command
```

---

## API Reference

### `POST /process`

**Request:**
```json
{ "command": "open youtube" }
```

**Response (`ActionResponse`):**
```json
{
  "action": "open_url",
  "message": "Opening YouTube",
  "data": { "url": "https://youtube.com" }
}
```

**Action types:** `speak` · `open_url` · `play_song` · `news` · `ai_reply` · `error`

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Optional* | Enables AI fallback replies via GPT-4o-mini |
| `NEWS_API_KEY` | Optional* | Enables live news headlines from NewsAPI |

*The server runs without these keys but those features will return a graceful error message.

---

## Tech Stack

- **Backend:** Python · FastAPI · Uvicorn · OpenAI SDK · Requests
- **Frontend:** HTML · CSS · JavaScript · Web Speech API
- **Desktop audio:** gTTS · pygame · pyttsx3 · SpeechRecognition
- **AI:** OpenAI GPT-4o-mini
- **News:** [NewsAPI](https://newsapi.org)
