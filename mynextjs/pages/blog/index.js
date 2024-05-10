// pages/blog/index.js

import { useEffect, useState } from "react";

export async function getServerSideProps(context) {

  // http://localhost:3000 에서의 쿠키를 API 요청에 활용
  const headers = {
    Cookie: context.req.headers.cookie,
  };
  console.log("headers: ", headers);

  const url = "http://localhost:8000/blog/whoami/";
  const response = await fetch(url, { headers });
  const responseText = `상태코드: ${response.status}

${await response.text()}`;

  // props로 전달한 값이 컴포넌트의 속성값으로 주입
  return { props: { message: responseText } };
}

function WhoamiPage({ message }) {
  // const [message, setMessage] = useState("no message");

  // 컴포넌트 초기화 시에 1회만 실행.
  // useEffect(() => {
  //   fetch("http://localhost:8000/blog/whoami/")
  //     .then((response) => response.text())
  //     .then((responseText) => {
  //       setMessage(responseText);
  //     });
  // }, []);

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
