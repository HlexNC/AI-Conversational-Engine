const express = require("express");
const fs = require("fs");
const path = require("path");
const WebSocket = require("ws");

const app = express();
const port = 3000;

// Create WebSocket server
const server = require("http").createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.json());
app.use(express.static(path.join(__dirname, "../client")));

// Serve chat_interface.html file on root path
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../client/chat_interface.html"));
});

function broadcastMessage(message) {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// Connect to Python WebSocket server
const pythonWebSocketUrl = "ws://localhost:8765";
const pythonWs = new WebSocket(pythonWebSocketUrl);

pythonWs.on("open", () => {
  console.log("Connected to Python WebSocket server");
});

pythonWs.on("message", (data) => {
  fs.appendFileSync("messages.jsonl", data + "\n");
  broadcastMessage(data);
});

// Handle WebSocket connections
wss.on("connection", (ws) => {
  console.log("Client connected");

  // Send stored messages to the client
  const messages = fs
    .readFileSync("messages.jsonl", "utf-8")
    .split("\n")
    .filter((line) => line)
    .map((line) => JSON.parse(line));

  messages.forEach((message) => {
    ws.send(JSON.stringify(message));
  });

  // Handle incoming messages from the client
  ws.on("message", (data) => {
    fs.appendFileSync("messages.jsonl", data + "\n");
    broadcastMessage(data);

    // Forward the message to the Python WebSocket server
    pythonWs.send(data);
  });
});

app.get("/messages", (req, res) => {
  const messages = fs
    .readFileSync("messages.jsonl", "utf-8")
    .split("\n")
    .filter((line) => line)
    .map((line) => JSON.parse(line));
  res.json(messages);
});

server.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
