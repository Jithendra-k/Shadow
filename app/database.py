from sqlmodel import SQLModel, Session, create_engine
from pathlib import Path

DB_PATH = Path("shadow_chat.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

def get_session():
    return Session(engine)

def init_db():
    SQLModel.metadata.create_all(engine)
