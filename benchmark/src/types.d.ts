export type Screening = {
  screening_id: string;
  title: string;
};
export type Currency = "GBP" | "USD" | "PLN";
export type Reservation = {
  customer_id: string;
  screening_id: string;
  reservation_number: string;
  amount: string;
  currency: Currency;
  details: object | string;
  seats_data: ([string, number] | [])[];
};
export type Options = {
  mode: string;
  delay: number;
  number: number;
  iterations: number;
  verbose: boolean;
};
export type ScreeningDetail = {
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

export type DoubleBookedSeats = {
  doubleBookedSeats: {
    [key: string]: number;
  };
  movie: string;
};
