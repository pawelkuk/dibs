export type Screening = {
  screening_id: string;
  movie: string;
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
  errorMargin: number;
  numbersOfScreenings: number;
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

export type Payment = {
  payment_id: string;
  user_id: string;
  status: string;
};

export type Ticket = {
  ticket_id: string;
  reservation_id: string;
  status: string;
  ticket_url: string;
};

export type DataPoint = {
  t: number;
  value: number;
};
