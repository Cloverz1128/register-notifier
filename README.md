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

The frontend runs on http://localhost:5173

The backend API runs on http://localhost:8000

```bash
# Create and activate virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload

# Run frontent
cd frontend
npm install
npm run dev

# Run pytest 
PYTHONPATH=. pytest -v
```

## Future Improvements