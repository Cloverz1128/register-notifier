from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.user import RegisterRequest, LoginRequest
from app.api.broadcast.sse import broadcaster
from app.db import engine

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/api/register")
async def register_api(data: RegisterRequest, response: Response):
    hashed_password = pwd_context.hash(data.password)
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == data.email)).first()
        if existing:
            return JSONResponse(status_code=400, content={"error": "User already exists"})

        user = User(email=data.email, hashed_password=hashed_password)
        session.add(user)
        session.commit()

    # set new cookie
    response.set_cookie(key="user", value=data.email, httponly=True)
    await broadcaster.broadcast(
        event_type="register",
        data=f"{data.email} registered"
    )

    return {"message": "Registered successfully"}

@router.post("/api/login")
def login_api(data: LoginRequest, response: Response):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == data.email)).first()
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            return JSONResponse(status_code=401, content={"error": "Invalid credentials"})

    response.set_cookie(key="user", value=data.email, httponly=True)
    return {"message": "Login successful"}

@router.post("/api/logout")
def logout_api(response: Response):
    response.delete_cookie("user")
    return {"message": "Logged out"}

@router.get("/api/welcome")
def get_user_info(request: Request):
    user_email = request.cookies.get("user")
    if not user_email:
        return JSONResponse(status_code=401, content={"error": "Not logged in"})
    return {"email": user_email}
