// src/index.js

import {createRoot} from "react-dom/client";

function App() {
  return (
    <div>
      <h1>Hello React.</h1>
    </div>
  );
}

// js 단에서 리액트 컴포넌트를 렌더링할 요소를 지정
const rootEl = document.getElementById("root");
const root = createRoot(rootEl)
root.render(<App />);
