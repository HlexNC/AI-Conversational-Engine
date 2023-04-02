const chatMessages = document.querySelector("#messages");
const chatInput = document.querySelector("#message");

// Function to add a new message to the chat
function addMessage(message, role) {
    const newMessage = document.createElement("div");
    newMessage.classList.add("message");

    const roleLabel = document.createElement("span");
    roleLabel.classList.add("label");
    roleLabel.textContent = (role === "bot" ? "UNICorn" : "User") + ": ";
    newMessage.appendChild(roleLabel);

    const messageText = document.createElement("span");
    messageText.classList.add("message-text", role + "-input");
    messageText.textContent = message;
    newMessage.appendChild(messageText);

    chatMessages.appendChild(newMessage);
}

// Function to handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    const message = chatInput.value;
    if (message) {
        addMessage(message, "user");
        chatInput.value = "";
        fetch("/chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message, role: "user" }),
        });
    }
}

// Function to load messages from the server
async function loadMessages() {
    const response = await fetch("/messages");
    const messages = await response.json();
    messages.forEach((message) => {
        addMessage(message.message, message.role);
    });
}

// Add event listener for form submission
chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        handleFormSubmit(event);
    }
});

// Load messages from the server
loadMessages();