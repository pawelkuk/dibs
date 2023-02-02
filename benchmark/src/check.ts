import { API_URL } from "./constants";
import axios, { AxiosError } from "axios";
import { Screening, ScreeningDetail } from "./types";
import { handleError } from "./utils";

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

async () => {
  const screeningsResponse = await getScreenings();
  if (!screeningsResponse) {
    return;
  }
  const screeningDetails = (
    await getScreeningDetails(screeningsResponse)
  ).filter(notEmpty);
};
