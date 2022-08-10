from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://backend_user:{os.getenv('BACKEND_PASSWORD')}@db:3306/{os.getenv('MYSQL_DATABASE')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
