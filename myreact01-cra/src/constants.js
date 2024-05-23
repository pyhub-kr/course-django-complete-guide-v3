// src/constants.js : 환경변수 로딩을 위한 파일
//  - 일관성 : 모든 환경 변수의 변환 및 처리 로직이 한 곳에 모여 있어 일관성을 유지할 수 있습니다.
//  - 가독성 : 환경 변수를 사용하는 곳마다 process.env.REACT_APP_...과 같은 긴 참조 대신,
//            단순하고 명확한 변수 이름을 사용할 수 있습니다. 이는 코드의 가독성을 높여줍니다.

// 문자열을 boolean 값으로 변환하는 함수
const toBoolean = (str) => {
  const lowerStr = (str || "").toLowerCase();
  return lowerStr === "1" || lowerStr.startsWith("t");
};

// 디폴트: "http://localhost:8000/
const API_HOST = process.env.REACT_APP_API_HOST || "http://localhost:8000";

// 0 : no timeout
const API_TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT) || 0;

const API_WITH_CREDENTIALS = toBoolean(
  process.env.REACT_APP_API_WITH_CREDENTIALS,
);

const LOGIN_URL =
  process.env.REACT_APP_LOGIN_URL || `${API_HOST}/accounts/login/`;
const LOGOUT_URL =
  process.env.REACT_APP_LOGOUT_URL || `${API_HOST}/accounts/logout/`;
const SIGNUP_URL =
  process.env.REACT_APP_LOGIN_URL || `${API_HOST}/accounts/signup/`;
const PROFILE_URL =
  process.env.REACT_APP_LOGIN_URL || `${API_HOST}/accounts/profile/`;

export {
  API_HOST,
  API_TIMEOUT,
  API_WITH_CREDENTIALS,
  LOGIN_URL,
  LOGOUT_URL,
  SIGNUP_URL,
  PROFILE_URL,
};
