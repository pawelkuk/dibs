const express = require("express");
const app = express();
const http = require("http");
const axios = require('axios');

const server = http.createServer(app);
const { Server } = require("socket.io");
global.state = {};
const bodyParser = require("body-parser");

(async () => {
  try {
    const response = await axios.get('http://app:80/screenings/76388a51-1fa6-428f-839f-32a1e5091aab/')
    state = response.data
    console.log("state set")
  } catch (error) {
    console.log(error);
  }
})();
app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.post("/update", (req, res) => {
  console.log(state);
});
io.on("connection", (socket) => {
  console.log("a user connected");
  socket.on("disconnect", () => {
    console.log("user disconnected");
  });
});

server.listen(3001, () => {
  console.log("listening on *:3001");
});
