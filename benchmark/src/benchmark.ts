import axios, { AxiosError } from "axios";
import { v4 as uuidv4 } from "uuid";
import { API_URL } from "./constants";
import { Options, Reservation, Screening, ScreeningDetail } from "./types";
import { handleError } from "./utils";
import { performance } from "perf_hooks";

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
  const successList: number[] = [];
  const errorList: number[] = [];
  console.log("starting benchmark");
  for (let i = 0; i < options.iterations; i++) {
    console.log("next iter!");
    try {
      const screeningsResponse = await axios.get<Screening[]>(
        `${API_URL}/screenings/`
      );
      const reqs = screeningsResponse.data.map(async (screening) => {
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
            const resReqs = reservationData.map(async (reservation) => {
              console.log(reservation.seats_data);
              console.log(options.mode);
              let start = performance.now();
              try {
                const res = await axios.post(
                  `${API_URL}/${options.mode}`,
                  reservation
                );
                let end = performance.now();
                successList.push(end - start);
              } catch (error) {
                let end = performance.now();
                errorList.push(end - start);
                handleError(error as AxiosError);
              }
              // console.log(reservation.seats_data);
            });
            await Promise.all(resReqs);
          }
        } catch (error) {
          handleError(error as AxiosError);
        }
      });
      await Promise.all(reqs);
    } catch (error) {
      handleError(error as AxiosError);
    }
    await sleep(options.delay);
  }
  const successStats = computeStats(successList);
  const errorStats = computeStats(errorList);
  const totalStats = computeStats(successList.concat(errorList));
  console.log("###### success stats ######");
  console.log("avg: ", successStats[0]);
  console.log("min: ", successStats[1]);
  console.log("max: ", successStats[2]);
  console.log("median: ", successStats[3]);
  console.log("number of successes: ", successList.length);
  console.log("###### error stats ######");
  console.log("avg: ", errorStats[0]);
  console.log("min: ", errorStats[1]);
  console.log("max: ", errorStats[2]);
  console.log("median: ", errorStats[3]);
  console.log("number of errors: ", errorList.length);
  console.log("###### total stats ######");
  console.log("avg: ", totalStats[0]);
  console.log("min: ", totalStats[1]);
  console.log("max: ", totalStats[2]);
  console.log("median: ", totalStats[3]);
  console.log("number of requests: ", successList.length + errorList.length);
}

function computeStats(times: number[]) {
  const total = times.reduce((a, b) => a + b, 0);
  const avg = total / times.length;
  const min = Math.min(...times);
  const max = Math.max(...times);
  const median = times.sort()[Math.floor(times.length / 2)];
  return [avg, min, max, median] as const;
}

export default main;
