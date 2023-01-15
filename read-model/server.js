const express = require("express");
const app = express();
const http = require("http");
const axios = require("axios");
const EventEmitter = require("events").EventEmitter;
const server = http.createServer(app);
const { Server } = require("socket.io");
global.state = new Map();
const bodyParser = require("body-parser");
const emitter = new EventEmitter();

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

getState = async (backoff) => {
  try {
    const response = await axios.get("http://app:80/screenings/");
    const screenings = response.data;
    screenings.forEach((obj) => {
      const screeningId = obj["screening_id"];
      axios
        .get(`http://app:80/screenings/${screeningId}/`)
        .then((res) => {
          state.set(screeningId, res.data);
          console.log(`${screeningId} screening data ready`);
          emitter.emit("state-change", screeningId);
        })
        .catch((error) => console.log(error.message));
    });
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
  try {
    screeningId = req.body["screening_id"];
    state.set(screeningId, req.body);
    emitter.emit("state-change", screeningId);
  } catch (error) {
    return res.send({ error: error.message });
  }
  return res.send({ status: "ok" });
});
io.on("connection", (socket) => {
  socket.on("screening", (screeningId) => {
    console.log(`user connected to ${screeningId}`);
    socket.join(screeningId);
    socket.emit("state-change", state.get(screeningId));
  });
  console.log("a user connected");
  socket.on("disconnect", () => {
    // socket.leave()
    console.log("user disconnected");
  });
});
emitter.on("state-change", (screeningId) => {
  console.log(`update front ${screeningId}`);
  io.sockets.in(screeningId).emit("state-change", state.get(screeningId));
});

server.listen(3001, () => {
  console.log("listening on *:3001");
});
