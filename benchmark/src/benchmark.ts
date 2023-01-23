import axios, { AxiosError } from "axios";
import { v4 as uuidv4 } from "uuid";
type Screening = {
  screening_id: string;
  title: string;
};
type Currency = "GBP" | "USD" | "PLN";
type Reservation = {
  customer_id: string;
  screening_id: string;
  reservation_number: string;
  amount: string;
  currency: Currency;
  details: object | string;
  seats_data: ([string, number] | [])[];
};
type Options = {
  mode: string;
  delay: number;
  number: number;
  iterations: number;
  verbose: boolean;
};
type ScreeningDetail = {
  screening_id: string;
  theatre: { theatre_id: string };
  movie: { title: string };
  reservations: {
    reservation_number: string;
    seats: string[];
    customer_id: string;
  }[];
  free_seats: string[];
};
const API_URL = "http://haproxy";
function handleError(err: AxiosError) {
  console.log(err.message);
}
function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function removeDuplicates(items: string[]): string[] {
  return items.filter((item, index) => items.indexOf(item) === index);
}

function pickSeats(seats: string[], max: number = 2): string[] {
  const picked_seats = [];
  for (let i = 0; i < max; i++) {
    let seat = seats[Math.floor(Math.random() * seats.length)];
    picked_seats.push(seat);
  }
  return removeDuplicates(picked_seats);
}
function extractSeat(seat: string): [string, number] | [] {
  const digitsPattern = /[0-9]+/g;
  const letterPattern = /[a-zA-Z]+/g;
  const letterMatch = seat.match(letterPattern);
  const digitsMatch = seat.match(digitsPattern);
  if (letterMatch === null || digitsMatch === null) {
    return [];
  } else {
    const row = letterMatch[0];
    const column = Number(digitsMatch[0]);
    return [row, column];
  }
}

function makeReservationData(
  screening: ScreeningDetail,
  n: number = 1000
): Reservation[] {
  const reservations: Reservation[] = Array.from(new Array(n).keys()).map(
    () => {
      const pickedSeats = pickSeats(
        screening.free_seats,
        Math.floor(Math.random() * 5) + 1
      );
      const reservation: Reservation = {
        customer_id: uuidv4(),
        screening_id: screening.screening_id,
        reservation_number: uuidv4(),
        amount: (10 * pickedSeats.length).toString(),
        currency: "GBP",
        details: { "agreement signed": true },
        seats_data: pickedSeats.map((seat: string) => extractSeat(seat)),
      };
      return reservation;
    }
  );
  return reservations;
}

async function main(options: Options) {
  console.log("starting benchmark");
  for (let i = 0; i < options.iterations; i++) {
    console.log("next iter!");
    try {
      const screeningsResponse = await axios.get<Screening[]>(
        `${API_URL}/screenings/`
      );
      screeningsResponse.data.map(async (screening: Screening) => {
        try {
          const screeningDetailResponse = await axios.get(
            `${API_URL}/screenings/${screening.screening_id}/`
          );
          const screeningDetail: ScreeningDetail = screeningDetailResponse.data;
          console.log(
            screeningDetail.screening_id,
            screeningDetail.free_seats.length
          );
          if (screeningDetail.free_seats) {
            const reservationData = makeReservationData(
              screeningDetail,
              options.number
            );
            reservationData.map(async (reservation) => {
              console.log(reservation.seats_data);
              try {
                const res = await axios.post(
                  `${API_URL}/${options.mode}`,
                  reservation
                );
              } catch (error) {
                handleError(error as AxiosError);
              }
              // console.log(reservation.seats_data);
            });
          }
        } catch (error) {
          handleError(error as AxiosError);
        }
      });
    } catch (error) {
      handleError(error as AxiosError);
    }
    await sleep(options.delay);
  }
}

export default main;
