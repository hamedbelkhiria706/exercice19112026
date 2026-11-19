import os
from pathlib import Path
from sqlalchemy import create_engine,event
from sqlalchemy.orm import sessionmaker, declarative_base

DB_PATH = Path(__file__).resolve().parents[4] / "app.db"
DATABSE_URI = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(
    DATABSE_URI
)
@event.listens_for(engine,'connect')
def enable_foreign_keys(dbapi_connection,connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.close()

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind = engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()