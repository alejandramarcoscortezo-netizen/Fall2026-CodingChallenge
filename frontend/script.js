const API_URL = "http://127.0.0.1:5000";

let selectedCollectionId = null;

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

        const name = document.createElement("span");
        name.className = "collection-name";
        name.textContent = collection.name;

        name.addEventListener(
            "click",
            () => openCollection(collection.id)
        );

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener(
            "click",
            () => deleteCollection(collection.id)
        );

        element.appendChild(name);
        element.appendChild(deleteButton);
        container.appendChild(element);
    }
}


async function createCollection() {
    const input =
        document.getElementById("collection-name");

    const name = input.value.trim();

    if (!name) {
        alert("Please enter a collection name.");
        return;
    }

    const response =await fetch(
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

    if (!response.ok){
        alert("Could not create collection.");
        return;
    }

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
