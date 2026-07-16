"""
database.py - MongoDB Connection Setup
"""

from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env explicitly
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")



# Connect to Atlas
client = MongoClient(MONGO_URI)

# Database
db = client["url_shortener"]

# Collection
collection = db["urls"]