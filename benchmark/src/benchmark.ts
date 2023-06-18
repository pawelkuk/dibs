import axios, { AxiosError } from "axios";
import { v4 as uuidv4 } from "uuid";
import { API_URL } from "./constants";
import slugify from "slugify";
import {
  Options,
  Reservation,
  Screening,
  ScreeningDetail,
  DataPoint,
} from "./types";
import { handleError } from "./utils";
import { performance } from "perf_hooks";
import fs from "fs";

function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function createNewScreening() {
  axios.post(`${API_URL}/screenings/`, {});
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
  for (let j = 0; j < options.numbersOfScreenings; j++) {
    console.log(`Start movie ${j + 1}!`);
    const successList: DataPoint[] = [];
    const errorList: DataPoint[] = [];
    const expStart = performance.now();
    const movieTitles: Screening[] = [];
    let seatsReserved = false;
    for (let i = 0; i < options.iterations; i++) {
      console.log("next iter!");
      try {
        const screeningsResponse = await axios.get<Screening[]>(
          `${API_URL}/screenings/`
        );
        if (seatsReserved) {
          const resps = screeningsResponse.data.map(async (screening) => {
            const resp = await axios.patch<Screening[]>(
              `${API_URL}/screenings/${screening.screening_id}/mark_as_full/`
            );
            if (resp.status !== 200) {
              throw Error("Could not mark screening as full! Debug :(");
            }
          });
          await Promise.all(resps);
          const res = await axios.post(
            `${API_URL}/screenings/partially_booked/`,
            { clean: true }
          );
          if (res.status !== 200) {
            throw Error("Could not create new screening! Debug :(");
          }
          seatsReserved = false;
          break;
        }
        const reqs = screeningsResponse.data.map(async (screening) => {
          try {
            movieTitles.push(screening);
            const screeningDetailResponse = await axios.get(
              `${API_URL}/screenings/${screening.screening_id}/`
            );
            const screeningDetail: ScreeningDetail =
              screeningDetailResponse.data;
            console.log(
              screeningDetail.screening_id,
              screeningDetail.free_seats.length
            );
            if (screeningDetail.free_seats.length > options.errorMargin) {
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
                  successList.push({
                    value: end - start,
                    t: end - expStart,
                  });
                } catch (error) {
                  let end = performance.now();
                  errorList.push({
                    value: end - start,
                    t: end - expStart,
                  });
                  handleError(error as AxiosError);
                }
                // console.log(reservation.seats_data);
              });
              await Promise.all(resReqs);
            } else {
              seatsReserved = true;
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
    writeDataToFile(successList, errorList, movieTitles[0], options, expStart);
    console.log({ movieTitles });
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
    console.log(`Movie ${j + 1} finished!`);
  }
}

function computeStats(times: DataPoint[]) {
  const total = times.reduce((a, b) => a + b.value, 0);
  const avg = total / times.length;
  const min = Math.min(...times.map((t) => t.value));
  const max = Math.max(...times.map((t) => t.value));
  const median = times.sort((a, b) => a.value - b.value)[
    Math.floor(times.length / 2)
  ];
  return [avg, min, max, median] as const;
}

function writeDataToFile(
  successData: DataPoint[],
  errorData: DataPoint[],
  screening: Screening,
  options: Options,
  expStart: number
) {
  const fName = getFileName(screening, options, expStart);
  const headers = "time,reservation_duration,was_successful\n";
  const csv =
    headers +
    successData.map((d) => `${d.t},${d.value},${true}`).join("\n") +
    "\n" +
    errorData.map((d) => `${d.t},${d.value},${false}`).join("\n");
  console.log(csv);
  fs.writeFileSync(`/data/${fName}`, csv);
}
function getFileName(screening: Screening, options: Options, expStart: number) {
  const movie = slugify(screening.movie);
  return `${Math.floor(expStart)}_${movie}_${options.mode}_${
    options.number
  }.csv`;
}

export default main;
