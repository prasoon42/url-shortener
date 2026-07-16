"""
main.py - FastAPI Application (Entry Point)

This is the heart of our backend. It defines all the API endpoints
that the frontend talks to.

How it works:
  1. Frontend sends an HTTP request (e.g., POST /shorten)
  2. FastAPI receives it and runs the matching function
  3. The function talks to MongoDB and returns a response
  4. Frontend displays the response to the user
"""

import string
import random
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from database import collection
from models import URLRequest, URLResponse

# ─── Create the FastAPI app ───────────────────────────────────────
app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener built with FastAPI and MongoDB",
    version="1.0.0",
)

# ─── CORS Middleware ──────────────────────────────────────────────
# CORS (Cross-Origin Resource Sharing) allows our frontend
# (running on a different port) to talk to our backend.
# Without this, the browser would block requests from the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (fine for learning projects)
    allow_credentials=True,
    allow_methods=["*"],      # Allow all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"],      # Allow all headers
)


# ─── Helper Function ─────────────────────────────────────────────
def generate_short_code(length: int = 6) -> str:
    """
    Generate a random 6-character short code.
    
    Uses letters (a-z, A-Z) and digits (0-9).
    Example output: "aB3kZ9"
    
    We also check MongoDB to make sure the code is unique.
    """
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    while True:
        # Pick 6 random characters
        short_code = "".join(random.choices(characters, k=length))
        # Check if this code already exists in the database
        if not collection.find_one({"short_code": short_code}):
            return short_code  # It's unique, so we can use it


# ─── API Endpoints ───────────────────────────────────────────────

@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    """
    POST /shorten — Create a shortened URL.

    What happens:
      1. Receive the original URL from the frontend
      2. Generate a unique 6-character short code
      3. Save both to MongoDB
      4. Return the shortened URL to the frontend
    """
    # Generate a unique short code
    short_code = generate_short_code()

    # Create the document to store in MongoDB
    url_document = {
        "original_url": request.original_url,
        "short_code": short_code,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "clicks": 0,
    }

    # Insert the document into MongoDB
    collection.insert_one(url_document)

    # Build and return the response
    return URLResponse(
        original_url=request.original_url,
        short_code=short_code,
        short_url=f"http://localhost:8000/{short_code}",
        clicks=0,
        created_at=url_document["created_at"],
    )


@app.get("/urls")
def get_all_urls():
    """
    GET /urls — Fetch all stored URLs.

    This endpoint returns every shortened URL in the database.
    The frontend uses this to display the list of previously shortened URLs.
    """
    urls = []
    # Find all documents in the collection
    for doc in collection.find():
        urls.append(
            URLResponse(
                original_url=doc["original_url"],
                short_code=doc["short_code"],
                short_url=f"http://localhost:8000/{doc['short_code']}",
                clicks=doc["clicks"],
                created_at=doc["created_at"],
            )
        )
    return urls


@app.delete("/delete/{short_code}")
def delete_url(short_code: str):
    """
    DELETE /delete/{short_code} — Delete a shortened URL.

    Finds the document by its short_code and removes it from MongoDB.
    Returns an error if the short code doesn't exist.
    """
    # Try to delete the document
    result = collection.delete_one({"short_code": short_code})

    # Check if anything was actually deleted
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {"message": "URL deleted successfully"}


@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    """
    GET /{short_code} — Redirect to the original URL.

    This is the core feature! When someone visits:
      http://localhost:8000/abc123
    
    We look up "abc123" in MongoDB, increment the click count,
    and redirect them to the original URL.
    """
    # Look up the short code in MongoDB
    url_doc = collection.find_one({"short_code": short_code})

    # If not found, return a 404 error
    if not url_doc:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Increment the click counter by 1
    collection.update_one(
        {"short_code": short_code},
        {"$inc": {"clicks": 1}},
    )

    # Redirect the user to the original URL
    return RedirectResponse(url=url_doc["original_url"])
