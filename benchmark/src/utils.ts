import { AxiosError } from "axios";

export function handleError(err: AxiosError) {
  console.log(err.message);
}
