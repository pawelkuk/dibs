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
};

function sleep(ms: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

async function main() {
  while (true) {
    await sleep(2000);
    await axios
      .get<Screening[]>("http://app/screenings")
      .then((res: AxiosResponse) => {
        res.data.map((screening: Screening) => {
          axios
            .get(`http://app/screenings/${screening.screening_id}/`)
            .then((res: AxiosResponse) => {
              let screeningDetail: ScreeningDetail = res.data;
              console.log(screeningDetail.movie.title);
              console.log(screeningDetail.reservations.flatMap((r) => r.seats));
            });
        });
      });
  }
}

main();
