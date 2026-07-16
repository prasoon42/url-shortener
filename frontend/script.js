/**
 * script.js - Frontend Logic
 *
 * This file handles all communication between the webpage and the FastAPI backend.
 * We use the Fetch API (built into every browser) to send HTTP requests.
 */

// ─── Configuration ──────────────────────────────────────────────
// The base URL of our FastAPI backend
const API_BASE = "http://localhost:8000";


// ─── Load all URLs when the page first opens ────────────────────
// This runs automatically when the page loads
window.addEventListener("DOMContentLoaded", () => {
    fetchAllURLs();
});


// ─── Shorten URL ────────────────────────────────────────────────
/**
 * Called when the user clicks the "Shorten URL" button.
 *
 * Steps:
 *   1. Get the URL from the input box
 *   2. Send a POST request to /shorten with the URL
 *   3. Display the shortened URL in the result section
 *   4. Refresh the list of all URLs
 */
async function shortenURL() {
    const input = document.getElementById("url-input");
    const originalURL = input.value.trim();

    // Basic validation — make sure the input isn't empty
    if (!originalURL) {
        alert("Please enter a URL!");
        return;
    }

    try {
        // Send POST request to the backend
        const response = await fetch(`${API_BASE}/shorten`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ original_url: originalURL }),
        });

        // Parse the JSON response
        const data = await response.json();

        // Show the result section
        const resultSection = document.getElementById("result-section");
        resultSection.classList.remove("hidden");

        // Display the short URL as a clickable link
        const shortURLLink = document.getElementById("short-url");
        shortURLLink.href = data.short_url;
        shortURLLink.textContent = data.short_url;

        // Clear the input box
        input.value = "";

        // Refresh the URL list to show the new one
        fetchAllURLs();
    } catch (error) {
        alert("Error shortening URL. Is the backend running?");
        console.error("Error:", error);
    }
}


// ─── Copy URL to Clipboard ─────────────────────────────────────
/**
 * Copies the shortened URL to the clipboard when "Copy" is clicked.
 */
function copyURL() {
    const shortURL = document.getElementById("short-url").textContent;
    navigator.clipboard.writeText(shortURL).then(() => {
        // Briefly change button text to show it worked
        const btn = document.querySelector(".copy-btn");
        btn.textContent = "Copied!";
        setTimeout(() => {
            btn.textContent = "Copy";
        }, 1500);
    });
}


// ─── Fetch All URLs ─────────────────────────────────────────────
/**
 * Fetches all shortened URLs from the backend and displays them.
 *
 * This is called:
 *   - When the page first loads
 *   - After creating a new short URL
 *   - After deleting a URL
 */
async function fetchAllURLs() {
    try {
        const response = await fetch(`${API_BASE}/urls`);
        const urls = await response.json();

        const urlsList = document.getElementById("urls-list");

        // If there are no URLs, show a friendly message
        if (urls.length === 0) {
            urlsList.innerHTML =
                '<p class="empty-message">No URLs shortened yet. Try one above!</p>';
            return;
        }

        // Build HTML for each URL card
        urlsList.innerHTML = urls
            .map(
                (url) => `
            <div class="url-card">
                <div class="url-info">
                    <a class="short-link" href="${url.short_url}" target="_blank">
                        ${url.short_url}
                    </a>
                    <span class="original-link" title="${url.original_url}">
                        ${url.original_url}
                    </span>
                </div>
                <div class="url-meta">
                    <span class="clicks-badge">${url.clicks} clicks</span>
                    <button class="delete-btn" onclick="deleteURL('${url.short_code}')">
                        Delete
                    </button>
                </div>
            </div>
        `
            )
            .join("");
    } catch (error) {
        console.error("Error fetching URLs:", error);
    }
}


// ─── Delete URL ─────────────────────────────────────────────────
/**
 * Deletes a shortened URL by its short code.
 *
 * Called when the user clicks the "Delete" button on a URL card.
 */
async function deleteURL(shortCode) {
    // Ask for confirmation before deleting
    if (!confirm("Are you sure you want to delete this URL?")) {
        return;
    }

    try {
        await fetch(`${API_BASE}/delete/${shortCode}`, {
            method: "DELETE",
        });

        // Refresh the list after deletion
        fetchAllURLs();
    } catch (error) {
        alert("Error deleting URL.");
        console.error("Error:", error);
    }
}
