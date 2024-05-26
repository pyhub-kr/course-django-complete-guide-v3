import Axios from "axios";
import { makeUseAxios } from "axios-hooks";
import { toast } from "react-toastify";
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
    } else if (error.response?.status === 400) {
      // 유효성 검사에 실패했을 때
      const errorMessages = error.response.data;
      toast.error(
        <>
          <ul className="list-unstyled">
            {Object.entries(errorMessages).map(([fieldName, fieldErrors]) => (
              <li key={fieldName}>
                <strong>{fieldName}</strong>: {fieldErrors.join(" ")}
              </li>
            ))}
          </ul>
        </>,
      );
    } else if (error.code === "ERR_CANCELED") {
      // 요청이 취소되었을 때
      /* skip */
    } else if (error.code === "ERR_NETWORK") {
      // 네트워크 오류
      console.error("에러 발생:", error);
      toast.error(`${error?.config?.url} 요청 중 네트워크 에러 발생`);
    } else if (error.response) {
      // 서버 응답이 있는 400, 401 외의 에러 상황
      // DRF 에러 응답 포맷에 따라 에러 메시지를 보여줍니다.
      const errorMessage = error.response.data?.detail || error.message;
      toast.error(`[${error.response.status}] ${errorMessage}`);
    } else {
      // 그 외의 에러 상황
      console.log("에러 발생:", error);
      toast.error(error.message);
    }

    return Promise.reject(error);
  },
);

const useApiAxios = makeUseAxios({
  axios: axiosInstance,
});

const apiRequest = async (url, method, data, raiseError = false) => {
  try {
    const response = await axiosInstance.request({
      method,
      url,
      data,
    });
    return { data: response.data, error: null, response };
  } catch (error) {
    if (error.response?.status === 400) {
      // Bad Request. 유효성 검사 에러
      return { data: null, error: error, response: null };
    } else {
      if (raiseError) throw error;
      return { data: null, error: error, response: null };
    }
  }
};

const makeRestApi = (baseUrl) => {
  return {
    getUrl(rel) {
      if (typeof rel === "string") {
        if (
          rel.startsWith("http://") ||
          rel.startsWith("https://") ||
          rel.startsWith("/")
        )
          return rel;
      }
      if (rel) {
        return `${baseUrl}${rel}/`;
      }
      return baseUrl;
    },

    async list(raiseError = false) {
      return apiRequest(this.getUrl(), "get", null, raiseError);
    },
    async detail(pk, raiseError = false) {
      return apiRequest(this.getUrl(pk), "get", null, raiseError);
    },
    async create(data, raiseError = false) {
      return apiRequest(this.getUrl(), "post", data, raiseError);
    },
    async update(pk, data, raiseError = false) {
      return apiRequest(this.getUrl(pk), "patch", data, raiseError);
    },
    async delete(pk, raiseError = false) {
      return apiRequest(this.getUrl(pk), "delete", null, raiseError);
    },
  };
};

export { useApiAxios, makeRestApi };
