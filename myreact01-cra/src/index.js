import React from "react";
import ReactDOM from "react-dom/client";
import { ToastContainer } from "react-toastify";
import "./index.css";
import App from "./App";
import App2 from "./App2";
import App3 from "./App3";
import App4 from "./App4";
import App5 from "./App5";
import reportWebVitals from "./reportWebVitals";
import App6 from "./App6";
import App7 from "./App7";
import App8 from "./App8";

// import "bootstrap/dist/css/bootstrap.min.css";

import "react-toastify/dist/ReactToastify.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <>
      {/*<App />*/}
      {/*<App2 />*/}
      {/*<App3 />*/}
      {/*<App4 />*/}
      {/*<App5 />*/}
      {/*<App6 />*/}
      {/*<App7 />*/}
      <App8 />
      <ToastContainer
        position="top-right"
        autoClose={3000}
        newestOnTop={true}
        closeOnClick={true}
        hideProgressBar={true}
        pauseOnHover={true}
        draggable={false}
      />
    </>
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
