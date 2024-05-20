import Axios from "axios";
import { makeUseAxios } from "axios-hooks";

const axiosInstance = Axios.create({
  baseURL: "https://pyhub.kr",
  // headers: {
  //   "Content-Type": "application/json",
  // },
});

const useApiAxios = makeUseAxios({
  axios: axiosInstance,
});

export { useApiAxios };
