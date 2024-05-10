// pages/blog/index.js

import { useState } from "react";

function WhoamiPage() {
  const [message, setMessage] = useState("no message");

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
