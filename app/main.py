from fastapi import FastAPI
from app.db import init_db
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

from app.api.auth import router as auth_router
from app.api.broadcast.sse import router as sse_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY) 

init_db()

app.include_router(auth_router)

app.include_router(sse_router)
