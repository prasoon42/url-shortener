
const API_BASE = "http://localhost:8000";


window.addEventListener("DOMContentLoaded", () => {
    fetchAllURLs();
});

async function shortenURL() {
    const input = document.getElementById("url-input");
    const originalURL = input.value.trim();

    // make sure the input isn't empty
    if (!originalURL) {
        alert("Please enter a URL!");
        return;
    }

    try {
        // send POST request to the backend
        const response = await fetch(`${API_BASE}/shorten`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ original_url: originalURL }),
        });

        // parse the JSON response
        const data = await response.json();

        // show the result section
        const resultSection = document.getElementById("result-section");
        resultSection.classList.remove("hidden");

        // display short URL as clickable link
        const shortURLLink = document.getElementById("short-url");
        shortURLLink.href = data.short_url;
        shortURLLink.textContent = data.short_url;

        // clear input box
        input.value = "";

        // refresh url list 
        fetchAllURLs();
    } catch (error) {
        alert("Error shortening URL. Is the backend running?");
        console.error("Error:", error);
    }
}

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


async function fetchAllURLs() {
    try {
        const response = await fetch(`${API_BASE}/urls`);
        const urls = await response.json();

        const urlsList = document.getElementById("urls-list");

        // if no URLs, show friendly message
        if (urls.length === 0) {
            urlsList.innerHTML =
                '<p class="empty-message">No URLs shortened yet. Try one above!</p>';
            return;
        }

        // build HTML for each URL card
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


async function deleteURL(shortCode) {
    // ask for confirmation before deleting
    if (!confirm("Are you sure you want to delete this URL?")) {
        return;
    }

    try {
        await fetch(`${API_BASE}/delete/${shortCode}`, {
            method: "DELETE",
        });

        // refresh list 
        fetchAllURLs();
    } catch (error) {
        alert("Error deleting URL.");
        console.error("Error:", error);
    }
}
