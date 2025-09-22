# Thomas Voice Assistant (Web Frontend + API)

## Backend

- Install deps:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

- Set API keys (optional but recommended):
```bash
export OPENAI_API_KEY=YOUR_OPENAI_KEY
export NEWS_API_KEY=YOUR_NEWSAPI_KEY
```

- Run server:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Health check: GET http://localhost:8000/health

## Frontend

- Open `web/index.html` in a browser (or serve via any static server).
- Configure backend URL in `web/script.js` if not running on localhost:8000.

Tip: To serve the frontend quickly with Python:
```bash
cd web
python3 -m http.server 5050
# then open http://localhost:5050
```

## Notes
- AI responses require `OPENAI_API_KEY`. News requires `NEWS_API_KEY`.
- The original microphone-based Python scripts remain unchanged; the web app uses the FastAPI API.
