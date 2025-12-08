from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def setup_database():
    with engine.connect() as connection:
        try:
            with open('database/functions.sql', 'r') as f:
                connection.execute(text(f.read()))
            connection.commit()
           
            with open('.setup_complete', 'w') as f:
                f.write('1')
        except FileNotFoundError:
            print("File database/functions.sql not found")
        except Exception as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            
            
import os
if not os.path.exists('.setup_complete'):
    setup_database()
    
Base = declarative_base()
