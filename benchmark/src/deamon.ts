import axios, { AxiosResponse } from "axios";
type Screening = {
  screening_id: string;
  title: string;
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
const API_URL = "http://app/screenings";

function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function main() {
  while (true) {
    await sleep(5000);
    await axios.get<Screening[]>(API_URL).then((res: AxiosResponse) => {
      res.data.map((screening: Screening) => {
        axios
          .get(`${API_URL}/${screening.screening_id}/`)
          .then((res: AxiosResponse) => {
            let screeningDetail: ScreeningDetail = res.data;
            console.log(screeningDetail.free_seats);
            console.log(screeningDetail.reservations.flatMap((r) => r.seats));
          });
      });
    });
  }
}

main();
