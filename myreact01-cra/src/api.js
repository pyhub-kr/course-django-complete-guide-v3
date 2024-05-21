import Axios from "axios";
import { makeUseAxios } from "axios-hooks";
import { API_HOST, API_TIMEOUT, API_WITH_CREDENTIALS } from "./constants";

const axiosInstance = Axios.create({
  baseURL: API_HOST,
  timeout: API_TIMEOUT,
  withCredentials: API_WITH_CREDENTIALS,
  // headers: {
  //   "Content-Type": "application/json",
  // },
});

const useApiAxios = makeUseAxios({
  axios: axiosInstance,
});

export { useApiAxios };
