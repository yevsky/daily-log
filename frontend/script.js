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

function renderEntries(entries) {
entriesContainer.innerHTML = "";


entries.forEach(entry => {
    const div = document.createElement("div");
    div.className = "entry";

    const tagText = entry.tag ? `#${entry.tag}` : "";
    const date = new Date(entry.created_at).toLocaleString();

    div.innerHTML = `
        <div><strong>${entry.content}</strong></div>
        <div class="tag">${tagText}</div>
        <div class="date">${date}</div>
    `;

    entriesContainer.appendChild(div);
});


}
