from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://backend_user:{os.getenv('BACKEND_PASSWORD')}@db:3306/{os.getenv('MYSQL_DATABASE')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=os.getenv("POOL_SIZE"),
    max_overflow=os.getenv("MAX_OVERFLOW"),
    pool_timeout=os.getenv("POOL_TIMEOUT"),
    pool_recycle=os.getenv("POOL_RECYCLE"),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
