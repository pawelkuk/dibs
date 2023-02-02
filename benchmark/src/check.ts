import { API_URL } from "./constants";
import axios, { AxiosError } from "axios";
import { DoubleBookedSeats, Screening, ScreeningDetail } from "./types";
import { handleError } from "./utils";
function Counter(array: string[]) {
  var count: { [key: string]: number } = {};
  array.forEach((val) => (count[val] = (count[val] || 0) + 1));
  return count;
}

function notEmpty<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const getScreenings = async () => {
  try {
    const screeningsResponse = await axios.get<Screening[]>(
      `${API_URL}/screenings/`
    );
    return screeningsResponse.data;
  } catch (error) {
    handleError(error as AxiosError);
  }
};

const getScreeningDetails = async (screenings: Screening[]) => {
  return await Promise.all(
    screenings.map(async (screening) => {
      try {
        const screeningDetailResponse = await axios.get(
          `${API_URL}/screenings/${screening.screening_id}/`
        );
        const screeningDetail: ScreeningDetail = screeningDetailResponse.data;
        return screeningDetail;
      } catch (error) {
        handleError(error as AxiosError);
      }
    })
  );
};
const findDoubleBooked = (
  screeningDetail: ScreeningDetail
): DoubleBookedSeats => {
  const allBookedSeats = screeningDetail.reservations
    .map((r) => r.seats)
    .flat();
  const counter = Counter(allBookedSeats);
  let k: keyof typeof counter;
  for (k in counter) if (counter[k] === 1) delete counter[k];
  return { doubleBookedSeats: counter, movie: screeningDetail.movie.title };
};

async function main() {
  console.log("start");
  const screeningsResponse = await getScreenings();
  if (!screeningsResponse) {
    console.log("no screenings found");
    return;
  }
  const screeningDetails = (
    await getScreeningDetails(screeningsResponse)
  ).filter(notEmpty);
  const doubleBooked = screeningDetails.map(findDoubleBooked);
  console.log(doubleBooked);
}
main();
