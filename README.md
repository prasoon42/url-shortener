# 🔗 URL Shortener

A simple URL shortener built with **FastAPI**, **MongoDB**, and **vanilla JavaScript**. This project takes a long URL and converts it into a short, shareable link.

> Built as a learning project to understand how backend APIs, databases, and frontend communication work together.

---

## 🛠️ Tech Stack

| Layer    | Technology              |
|----------|-------------------------|
| Frontend | HTML, CSS, JavaScript   |
| Backend  | Python, FastAPI, Uvicorn|
| Database | MongoDB Atlas, PyMongo  |
| DevOps   | Docker, Git             |

---

## 📁 Folder Structure

```
url-shortener/
│
├── backend/
│   ├── main.py              # FastAPI app with all API endpoints
│   ├── database.py          # MongoDB connection setup
│   ├── models.py            # Pydantic models for request/response
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Docker config for the backend
│
├── frontend/
│   ├── index.html           # Main webpage
│   ├── style.css            # Styling
│   └── script.js            # Frontend logic (API calls)
│
├── README.md
└── .gitignore
```

---

## ⚙️ How to Install

### Prerequisites

- Python 3.9+ installed
- A MongoDB Atlas account (free tier works)
- Git installed

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

### Step 2: Set Up a Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate        # On Mac/Linux
# venv\Scripts\activate         # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Your MongoDB URI

```bash
export MONGO_URI="your_mongodb_atlas_connection_string"
# On Windows: set MONGO_URI=your_mongodb_atlas_connection_string
```

---

## 🗄️ MongoDB Atlas Setup

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas) and create a free account.
2. Create a new **Cluster** (the free M0 tier is fine).
3. Click **"Connect"** → **"Connect your application"**.
4. Copy the connection string. It looks like:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `username` and `password` with your actual credentials.
6. Set this as your `MONGO_URI` environment variable (see Step 4 above).

> **Important:** Make sure to add your IP address to the **Network Access** whitelist in Atlas, or allow access from anywhere (`0.0.0.0/0`) for development.

---

## 🚀 How to Run

### Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

The API will be running at: `http://localhost:8000`

You can also see the auto-generated API docs at: `http://localhost:8000/docs`

### Open the Frontend

Simply open `frontend/index.html` in your browser. No server needed for the frontend!

```bash
# On Mac
open frontend/index.html

# On Windows
start frontend/index.html

# On Linux
xdg-open frontend/index.html
```

---

## 🐳 Running with Docker

### Build the Docker Image

```bash
cd backend
docker build -t url-shortener-backend .
```

### Run the Container

```bash
docker run -p 8000:8000 -e MONGO_URI="your_mongodb_atlas_connection_string" url-shortener-backend
```

---

## 🔌 API Endpoints

| Method   | Endpoint              | Description                    |
|----------|-----------------------|--------------------------------|
| `POST`   | `/shorten`            | Create a shortened URL         |
| `GET`    | `/urls`               | Get all shortened URLs         |
| `GET`    | `/{short_code}`       | Redirect to the original URL   |
| `DELETE` | `/delete/{short_code}`| Delete a shortened URL         |

### Example: Create a Short URL

**Request:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://google.com"}'
```

**Response:**
```json
{
    "original_url": "https://google.com",
    "short_code": "aB3kZ9",
    "short_url": "http://localhost:8000/aB3kZ9",
    "clicks": 0,
    "created_at": "2025-01-01 12:00:00"
}
```

---

## 🧠 How the Project Works

### 1. Frontend → Backend Communication

When you click "Shorten URL", the JavaScript `fetch()` function sends an HTTP POST request to `http://localhost:8000/shorten` with the long URL in the request body. FastAPI receives this, processes it, and sends back the short URL as JSON.

### 2. Backend → MongoDB Communication

FastAPI uses **PyMongo** to talk to MongoDB. When a new URL is shortened:
- A random 6-character code is generated
- A document is inserted into the `urls` collection
- The document contains: `original_url`, `short_code`, `created_at`, `clicks`

### 3. How URL Shortening Works

1. User enters: `https://www.google.com/search?q=very+long+url`
2. Backend generates a random code: `aB3kZ9`
3. Both are stored in MongoDB as a pair
4. The short URL becomes: `http://localhost:8000/aB3kZ9`

The "shortening" is simply a **mapping** — we store the long URL and give back a short code that points to it.

### 4. How Redirects Work

When someone visits `http://localhost:8000/aB3kZ9`:
1. FastAPI catches this request via the `GET /{short_code}` endpoint
2. It looks up `aB3kZ9` in MongoDB
3. It finds the original URL: `https://www.google.com/search?q=very+long+url`
4. It returns a `RedirectResponse`, which tells the browser to go to the original URL
5. The `clicks` counter is incremented by 1

### 5. How Docker is Used

Docker packages the backend into a **container** — a lightweight, isolated environment that includes Python, all dependencies, and our code. This means:
- Anyone can run the app without installing Python or dependencies
- It works the same on every computer
- It's ready for deployment to cloud platforms

---

## 📸 Screenshots

_Add screenshots of your running application here._

---

## 🚀 Future Improvements

- [ ] Add custom short codes (let users pick their own)
- [ ] Add URL validation (check if the URL is valid before shortening)
- [ ] Add expiration dates for short URLs
- [ ] Add QR code generation for each short URL
- [ ] Deploy to a cloud platform (AWS, Railway, Render)
- [ ] Add a dashboard with click analytics

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
