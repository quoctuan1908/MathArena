from contextlib import contextmanager
from src.database.core import SessionLocal

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()