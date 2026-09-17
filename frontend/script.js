const API_URL = "http://127.0.0.1:5000";


async function loadCollections() {
    const response = await fetch(
        `${API_URL}/collections`
    );

    const collections = await response.json();

    const container =
        document.getElementById("collections");

    container.innerHTML = "";

    for (const collection of collections) {
        const element =
            document.createElement("div");

        element.className = "collection";

        element.textContent = collection.name;

        container.appendChild(element);
    }
}


async function createCollection() {
    const input =
        document.getElementById("collection-name");

    const name = input.value.trim();

    if (!name) {
        return;
    }

    await fetch(
        `${API_URL}/collections`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name
            })
        }
    );

    input.value = "";

    await loadCollections();
}


document
    .getElementById("create-collection")
    .addEventListener(
        "click",
        createCollection
    );


loadCollections();