import Axios from "axios";
import { makeUseAxios } from "axios-hooks";
import { API_HOST, API_TIMEOUT, API_WITH_CREDENTIALS } from "./constants";

function createAxiosInstance(allowUnauthorized) {
  const config = {
    baseURL: API_HOST,
    timeout: API_TIMEOUT,
    withCredentials: API_WITH_CREDENTIALS,
    // headers: {
    //   "Content-Type": "application/json",
    // },
  };

  if (allowUnauthorized) {
    config.validateStatus = (status) =>
      (status >= 200 && status < 300) || status === 401;
  }

  return Axios.create(config);
}

const useApiAxios = (config, options) => {
  const allowUnauthorized = (options || {}).allowUnauthorized || false;
  const axiosInstance = createAxiosInstance(allowUnauthorized);
  const hook = makeUseAxios({ axios: axiosInstance });
  return hook(config, options);
};

// const useApiAxios = makeUseAxios({
//   axios: axiosInstance,
// });

export { useApiAxios };
