"""
database.py - MongoDB Connection Setup

This file handles the connection to MongoDB Atlas.
We use PyMongo (the official MongoDB driver for Python) to connect.
"""

from pymongo import MongoClient
import os

# ─── MongoDB Connection ───────────────────────────────────────────
# We read the connection string from an environment variable.
# This is better than hardcoding it because:
#   1. It keeps your credentials safe (not pushed to GitHub)
#   2. It makes switching between local and production easy

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create a MongoClient — this is our connection to MongoDB
client = MongoClient(MONGO_URI)

# Select (or create) a database called "url_shortener"
db = client["url_shortener"]

# Select (or create) a collection called "urls"
# A collection in MongoDB is like a table in SQL
collection = db["urls"]
