import "./App.css";
import React, { useState, useEffect } from "react";
import io from "socket.io-client";

const socket = io.connect(":3001");

const getSeats = () => {
  const row = [...Array(25).keys()].map((el) => el + 1);
  const alpha = Array.from(Array(26)).map((e, i) => i + 65);
  const alphabet = alpha.map((x) => String.fromCharCode(x));
  const seats = alphabet.map((char) => row.map((num) => char + num.toString()));
  return seats.flat();
};

function App(props) {
  const seats = getSeats();
  const [seatsAvailable, setSeatsAvailable] = useState([...seats]);
  const [seatsSelected, setSeatsSelected] = useState([]);
  const [seatsReserved, setSeatsReserved] = useState([]);
  const [isConnected, setIsConnected] = useState(socket.connected);

  useEffect(() => {
    socket.on("connect", () => {
      setIsConnected(true);
    });

    socket.on("disconnect", () => {
      setIsConnected(false);
    });

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("pong");
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
    setSeatsReserved(seatsReserved.concat(seats));
    setSeatsSelected([]);
  }
  return (
    <div>
      <div>
        <p>Connected: {"" + isConnected}</p>
      </div>
      <div>
        <h1>Dibs - Seat Reservation System</h1>
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
