from pydantic import BaseModel


class URLRequest(BaseModel):
    
    original_url: str

class URLResponse(BaseModel):
    
    original_url: str
    short_code: str
    short_url: str
    clicks: int
    created_at: str
