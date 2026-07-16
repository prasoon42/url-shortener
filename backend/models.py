"""
models.py - Pydantic Models

Pydantic models define the "shape" of data our API expects.
Think of them as blueprints — they validate incoming data automatically.
If someone sends bad data, FastAPI will return a clear error.
"""

from pydantic import BaseModel


class URLRequest(BaseModel):
    """
    This model defines what the client must send when creating a short URL.
    
    Example request body:
    {
        "original_url": "https://google.com"
    }
    """
    original_url: str


class URLResponse(BaseModel):
    """
    This model defines what we send back to the client.
    
    Example response:
    {
        "original_url": "https://google.com",
        "short_code": "abc123",
        "short_url": "http://localhost:8000/abc123",
        "clicks": 0,
        "created_at": "2025-01-01 12:00:00"
    }
    """
    original_url: str
    short_code: str
    short_url: str
    clicks: int
    created_at: str
