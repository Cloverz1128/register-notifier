from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)