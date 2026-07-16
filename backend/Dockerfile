# ─── Dockerfile for the URL Shortener Backend ────────────────────
#
# Docker lets you package your app so it runs the same everywhere.
# Think of it as a "lightweight virtual machine" for your app.
#
# To build:  docker build -t url-shortener-backend .
# To run:    docker run -p 8000:8000 -e MONGO_URI="your_mongo_uri" url-shortener-backend

# Step 1: Start with a Python base image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy requirements.txt first (for better Docker caching)
COPY requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the backend code
COPY . .

# Step 6: Expose port 8000 (so we can access the app)
EXPOSE 8000

# Step 7: Start the FastAPI server with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
