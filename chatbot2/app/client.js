const chatMessages = document.querySelector("#messages");
const chatInput = document.querySelector("#message");

// Connect to WebSocket server
const ws = new WebSocket("ws://localhost:3000");

console.log("Connecting to WebSocket server...");
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

// Listen for messages from the server
ws.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  addMessage(message.message, message.role);
});

// Function to handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    const message = chatInput.value;
    if (message) {
        addMessage(message, "user");
        chatInput.value = "";
        // Send the message to the server using WebSockets
        ws.send(JSON.stringify({ message, role: "user" }));
    }
}

// Add event listener for form submission
chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        handleFormSubmit(event);
    }
});

async function loadMessages() {
    const response = await fetch("http://localhost:3000/messages");
    const messages = await response.json();
    messages.forEach((message) => {
        addMessage(message.message, message.role);
    });
}
loadMessages();
