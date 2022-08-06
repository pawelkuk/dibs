import "./App.css";
import React, { useState } from "react";

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
  const [seatsReserved, setSeatsReserved] = useState([]);

  function onClickData(seat) {
    if (seatsReserved.indexOf(seat) > -1) {
      setSeatsAvailable(seatsAvailable.concat(seat));
      setSeatsReserved(seatsReserved.filter((res) => res !== seat));
    } else {
      setSeatsReserved(seatsReserved.concat(seat));
      setSeatsAvailable(seatsAvailable.filter((res) => res !== seat));
    }
  }

  return (
    <div>
      <h1>Dibs - Seat Reservation System</h1>
      <DrawGrid
        seat={seats}
        available={seatsAvailable}
        reserved={seatsReserved}
        onClickData={(seat) => onClickData(seat)}
      />
    </div>
  );
}

function DrawGrid(props) {
  function onClickSeat(seat) {
    props.onClickData(seat);
  }
  return (
    <div className="container">
      <table className="grid">
        <tbody>
          <tr>
            {props.seat.map((row) => (
              <td
                className={
                  props.reserved.indexOf(row) > -1 ? "reserved" : "available"
                }
                key={row}
                onClick={(e) => onClickSeat(row)}
              >
                {row}
              </td>
            ))}
          </tr>
        </tbody>
      </table>

      <AvailableList available={props.available} />
      <ReservedList reserved={props.reserved} />
    </div>
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

function ReservedList(props) {
  return (
    <div className="right">
      <h4>Reserved Seats: ({props.reserved.length})</h4>
      <ul>
        {props.reserved.map((res) => (
          <li key={res}>{res}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
