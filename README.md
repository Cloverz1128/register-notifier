# Register Notifier

A simple full-stack web app that demonstrates user authentication with real-time notifications using Server-Sent Events (SSE).

> Built with **FastAPI + React**.

## Features

- Register & Login with email + password
- Real-time notification on new user registration
- Frontend displays messages using Server-Sent Events (SSE)
- SQLite local storage for quick testing
- Pytest unit tests for backend APIs

## Quick Start

```bash
# Create and activate virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Edit .env if needed
cp .env.example .env

# Run backend
uvicorn app.main:app --reload

# Run frontent
cd frontend
npm install
npm run dev

# Run pytest 
PYTHONPATH=. pytest -v
```

## Default URLs
* Backend API: http://localhost:8000
* SSE endpoint: http://localhost:8000/sse
* Frontend (React): http://localhost:5173

## Future Improvements
* Persistent notification history (database-based)
* SSE reconnect logic with Last-Event-ID
* User inactivity auto-logout

## License
MIT License