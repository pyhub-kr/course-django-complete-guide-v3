// src/contexts/StatusContext.js

import { createContext, useContext } from "react";
import { useApiAxios } from "../api";

// StatusContext.Provider 내에서 Context를 사용하지 않으면, 이 값이 반환됩니다.
//  - undefined가 반환되면 StatusContext.Provider를 사용하지 않은 상황으로 간주합니다.
//  - 오류를 띄워 개발자가 고치도록 유도합니다.
const StatusContext = createContext(undefined);

function StatusProvider({ children }) {
  const [{ data: status = {} }] = useApiAxios({
    url: "/accounts/api/status/",
  });

  return (
    <StatusContext.Provider value={status}>{children}</StatusContext.Provider>
  );
}

function useStatusContext() {
  const status = useContext(StatusContext);
  if (status === undefined) {
    throw new Error("useStatusContext must be used within a StatusProvider");
  }
  return status;
}

export { StatusProvider, useStatusContext };
