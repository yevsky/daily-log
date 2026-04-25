const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("entry-form");
const contentInput = document.getElementById("content");
const tagInput = document.getElementById("tag");
const entriesContainer = document.getElementById("entries");

window.addEventListener("DOMContentLoaded", loadEntries);

form.addEventListener("submit", async (e) => {
e.preventDefault();

const content = contentInput.value;
const tag = tagInput.value || null;

await createEntry(content, tag);

contentInput.value = "";
tagInput.value = "";

await loadEntries();

});

async function loadEntries() {
    const response = await fetch(`${API_URL}/entries`);
    const data = await response.json();
    renderEntries(data);
}

async function createEntry(content, tag) {
    await fetch(`${API_URL}/entries`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({
        content: content,
        tag: tag
        })
    });
}

async function deleteEntry(id) {
    await fetch(`${API_URL}/entries/${id}`, {
        method: "DELETE"
    });
}

async function updateEntry(id, content, tag) {
    await fetch(`${API_URL}/entries/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content, tag })
    });
}

function renderEntries(entries) {
    entriesContainer.innerHTML = "";

    entries.forEach(entry => {
        const div = document.createElement("div");
        div.className = "entry";

        const tagText = entry.tag ? `#${entry.tag}` : "";
        const date = new Date(entry.created_at).toLocaleString();

        div.innerHTML = `
            <div class="entry-content">
                <strong>${entry.content}</strong>
                <div class="tag">${tagText}</div>
            </div>

            <div class="entry-actions">
                <span class="date">${date}</span>

                <button class="edit-btn" title="Edit">✏️</button>
                <button class="delete-btn" title="Delete">🗑️</button>
            </div>
        `;

        div.querySelector(".delete-btn").addEventListener("click", async () => {
            await deleteEntry(entry.id);
            await loadEntries();
        });

        div.querySelector(".edit-btn").addEventListener("click", async () => {
            const newContent = prompt("Edit content:", entry.content);
            if (newContent === null) return;

            const newTag = prompt("Edit tag:", entry.tag || "");
            if (newTag === null) return;

            await updateEntry(entry.id, newContent, newTag || null);
            await loadEntries();
        });

        entriesContainer.appendChild(div);
    });
}