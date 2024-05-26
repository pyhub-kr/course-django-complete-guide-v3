import Axios from "axios";
import { makeUseAxios } from "axios-hooks";
import {
  API_HOST,
  API_TIMEOUT,
  API_WITH_CREDENTIALS,
  LOGIN_URL,
} from "./constants";

const axiosInstance = Axios.create({
  baseURL: API_HOST,
  timeout: API_TIMEOUT,
  withCredentials: API_WITH_CREDENTIALS,
  // headers: {
  //   "Content-Type": "application/json",
  // },
});

axiosInstance.interceptors.request.use((config) => {
  // POST/PATCH/PUT/DELETE 요청에 대해 CSRF Token 헤더 자동 추가
  if (["post", "patch", "put", "delete"].includes(config.method)) {
    config.headers["X-CSRFToken"] = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
  }
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const next_url = window.location.href;
      window.location.href = `${LOGIN_URL}?next=${next_url}`;
    }
    return Promise.reject(error);
  },
);

const useApiAxios = makeUseAxios({
  axios: axiosInstance,
});

export { useApiAxios };
