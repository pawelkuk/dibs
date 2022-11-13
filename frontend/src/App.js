import "./App.css";
import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import axios from "axios";
import { Routes, Route, Link, useParams } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";

const API = "http://localhost:5005";
const getSeats = () => {
  const row = [...Array(25).keys()].map((el) => el + 1);
  const alpha = Array.from(Array(26)).map((e, i) => i + 97);
  const alphabet = alpha.map((x) => String.fromCharCode(x));
  const seats = alphabet.map((char) => row.map((num) => char + num.toString()));
  return seats.flat();
};

function ScreeningList(props) {
  const [screeningList, setScreeningList] = useState([]);
  useEffect(() => {
    axios
      .get(`${API}/screenings/`)
      .then((response) => {
        const data = response.data;
        setScreeningList(data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <ul>
      {screeningList.map((obj) => (
        <li key={obj.screening_id}>
          <Link to={`/screenings/${obj.screening_id}`}>{obj.movie}</Link>
        </li>
      ))}
    </ul>
  );
}

function ScreeningRoom(props) {
  const socket = io.connect(":3001");
  const seats = getSeats();
  const [seatsAvailable, setSeatsAvailable] = useState([...seats]);
  const [seatsSelected, setSeatsSelected] = useState([]);
  const [seatsReserved, setSeatsReserved] = useState([]);
  const [isConnected, setIsConnected] = useState(socket.connected);
  const { screeningId } = useParams();
  useEffect(() => {
    socket.on("connect", () => {
      socket.emit("screening", screeningId);
      setIsConnected(true);
    });

    socket.on("state-change", (state) => {
      const sr = [];
      state.reservations.map((res) => sr.push(...res.seats));
      setSeatsReserved(sr);
      setSeatsAvailable(
        seatsAvailable.filter((seat) => {
          return sr.findIndex((s) => s === seat) === -1;
        })
      );
    });
    socket.on("disconnect", () => {
      setIsConnected(false);
    });

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("state-change");
    };
  }, []);

  function onClickData(seat) {
    if (seatsReserved.indexOf(seat) > -1) return;
    if (seatsSelected.indexOf(seat) > -1) {
      setSeatsAvailable(seatsAvailable.concat(seat));
      setSeatsSelected(seatsSelected.filter((res) => res !== seat));
    } else {
      setSeatsSelected(seatsSelected.concat(seat));
      setSeatsAvailable(seatsAvailable.filter((res) => res !== seat));
    }
  }
  function onClickReservation(seats) {
    const digitsPattern = /[0-9]+/g;
    const letterPattern = /[a-zA-Z]+/g;
    const seatsData = seats.map((seat) => {
      const row = seat.match(letterPattern)[0];
      const column = seat.match(digitsPattern)[0];
      return [row, Number(column)];
    });
    axios
      .post(`${API}/make-reservation`, {
        customer_id: uuidv4(),
        screening_id: screeningId,
        reservation_number: uuidv4(),
        seats_data: seatsData,
      })
      .catch((error) => {
        alert(error.message);
      });
    setSeatsSelected([]);
  }
  return (
    <div>
      <div>
        <p>Connected: {"" + isConnected}</p>
      </div>
      <div>
        <h1>
          <Link to={"/"}>Dibs - Seat Reservation System</Link>
        </h1>
        <DrawGrid
          seat={seats}
          available={seatsAvailable}
          selected={seatsSelected}
          reserved={seatsReserved}
          onClickData={(seat) => onClickData(seat)}
          onClickReservation={onClickReservation}
        />
      </div>
    </div>
  );
}

function NotFound() {
  return (
    <div style={{ padding: "1rem" }}>
      <p>404 - not found</p>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<ScreeningList />} />
      <Route path="screenings/:screeningId" element={<ScreeningRoom />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

function DrawGrid(props) {
  function onClickSeat(seat) {
    props.onClickData(seat);
  }
  function getSeatType(seat) {
    if (props.reserved.indexOf(seat) > -1) return "reserved";
    if (props.selected.indexOf(seat) > -1) return "selected";
    return "available";
  }
  return (
    <div className="container">
      <table className="grid">
        <tbody>
          <tr>
            {props.seat.map((row) => (
              <td
                className={getSeatType(row)}
                key={row}
                onClick={(e) => onClickSeat(row)}
              >
                {row}
              </td>
            ))}
          </tr>
        </tbody>
      </table>

      <SelectedList selected={props.selected} />
      <MakeReservation
        selected={props.selected}
        onClickReservation={props.onClickReservation}
      />
      <AvailableList available={props.available} />
    </div>
  );
}

function MakeReservation(props) {
  return (
    <button onClick={(e) => props.onClickReservation(props.selected)}>
      Dibs!
    </button>
  );
}
function AvailableList(props) {
  const seatCount = props.available.length;
  return (
    <div className="left">
      <h4>
        Available Seats: ({seatCount === 0 ? "No seats available" : seatCount})
      </h4>
      <ul>
        {props.available.map((res) => (
          <li key={res}>{res}</li>
        ))}
      </ul>
    </div>
  );
}

function SelectedList(props) {
  return (
    <div className="right">
      <h4>Selected Seats: ({props.selected.length})</h4>
      <ul>
        {props.selected.map((res) => (
          <li key={res}>{res}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
