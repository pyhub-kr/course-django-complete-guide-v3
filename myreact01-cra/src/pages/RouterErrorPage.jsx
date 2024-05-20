// src/pages/RouterErrorPage.jsx

import { NavLink, useRouteError } from "react-router-dom";
import { Alert } from "react-bootstrap";

function RouterErrorPage() {
  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <Alert variant="danger">
        <Alert.Heading>404</Alert.Heading>
        <p>페이지를 찾을 수 없습니다.</p>
        <div>
          <NavLink to="/">홈으로</NavLink>
        </div>
      </Alert>
    </div>
  );
}

export default RouterErrorPage;
