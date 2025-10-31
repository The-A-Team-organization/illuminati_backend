import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "illuminaties")
    DATABASE_USER = os.getenv("DATABASE_USER", "admin")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "rootpass")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "3325")
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    SECRET_ENTRY_PASSWORD = os.getenv("SECRET_ENTRY_PASSWORD", "")