const express = require("express");
const app = express();
const http = require("http");
const axios = require("axios");
const EventEmitter = require("events").EventEmitter;
const server = http.createServer(app);
const { Server } = require("socket.io");
global.state = {};
const bodyParser = require("body-parser");
const emitter = new EventEmitter();

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

getState = async (backoff) => {
  try {
    const response = await axios.get(
      "http://app:80/screenings/76388a51-1fa6-428f-839f-32a1e5091aab/"
    );
    state = response.data;
    console.log("state ready");
    emitter.emit("state-change");
  } catch (error) {
    console.log(error);
    await sleep(backoff);
    await getState(2 * backoff);
  }
};

getState(1000);

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
  emitter.emit("state-change");
  return res.send({ status: "ok" });
});
io.on("connection", (socket) => {
  console.log("a user connected");
  socket.emit("state-change", state);
  socket.on("disconnect", () => {
    console.log("user disconnected");
  });
});
emitter.on("state-change", () => {
  console.log("update front");
  io.sockets.emit("state-change", state);
});

server.listen(3001, () => {
  console.log("listening on *:3001");
});
