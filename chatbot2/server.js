const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, ".")));

// Serve index.html file on root path
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// POST endpoint to receive messages from the client
app.post("/chatbot", (req, res) => {
  const message = req.body;
  fs.appendFileSync("messages.jsonl", JSON.stringify(message) + "\n");
  res.sendStatus(200);
});

// GET endpoint to return all messages
app.get("/messages", (req, res) => {
  const messages = fs
    .readFileSync("messages.jsonl", "utf-8")
    .split("\n")
    .filter((line) => line)
    .map((line) => JSON.parse(line));
  res.json(messages);
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});