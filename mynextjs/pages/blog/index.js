// pages/blog/index.js

import { useEffect, useState } from "react";

function WhoamiPage() {
  const [message, setMessage] = useState("no message");

  // 컴포넌트 초기화 시에 1회만 실행.
  useEffect(() => {
    fetch("http://localhost:8000/blog/whoami/")
      .then((response) => response.text())
      .then((responseText) => {
        setMessage(responseText);
      });
  }, []);

  return (
    <div>
      <h2>whoami</h2>
      <pre>{message}</pre>
      <hr />
      <small>by Next.js</small>
    </div>
  );
}

export default WhoamiPage;
