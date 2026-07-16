import string
import random
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from database import collection
from models import URLRequest, URLResponse

# create the fastAPI app 
app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener built with FastAPI and MongoDB",
    version="1.0.0",
)

# CORS middleware 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],      
)


# helper function 
def generate_short_code(length: int = 6) -> str:
  
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    while True:
        # Pick 6 random char
        short_code = "".join(random.choices(characters, k=length))
        # Check if code already exists in database
        if not collection.find_one({"short_code": short_code}):
            return short_code  


# API Endpoints

@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    
    short_code = generate_short_code()

    # create doc to store in mongoDb
    url_document = {
        "original_url": request.original_url,
        "short_code": short_code,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "clicks": 0,
    }

    # insert doc into mongoDb
    collection.insert_one(url_document)

    # return the response
    return URLResponse(
        original_url=request.original_url,
        short_code=short_code,
        short_url=f"http://localhost:8000/{short_code}",
        clicks=0,
        created_at=url_document["created_at"],
    )


@app.get("/urls")
def get_all_urls():
    
    urls = []
    
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
    
    
    result = collection.delete_one({"short_code": short_code})

    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {"message": "URL deleted successfully"}


@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    
    url_doc = collection.find_one({"short_code": short_code})

    
    if not url_doc:
        raise HTTPException(status_code=404, detail="Short URL not found")

    
    collection.update_one(
        {"short_code": short_code},
        {"$inc": {"clicks": 1}},
    )

    
    return RedirectResponse(url=url_doc["original_url"])
