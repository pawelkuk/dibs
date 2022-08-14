const express = require("express");
const app = express();
const http = require("http");
const axios = require('axios');

const server = http.createServer(app);
const { Server } = require("socket.io");
global.state = {};
const bodyParser = require("body-parser");

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

getState = async (backoff) => {
  try {
    const response = await axios.get('http://app:80/screenings/76388a51-1fa6-428f-839f-32a1e5091aab/')
    state = response.data
  } catch (error) {
    console.log(error);
    await sleep(backoff)
    await getState(2*backoff)
  }
};

getState(1000)

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
