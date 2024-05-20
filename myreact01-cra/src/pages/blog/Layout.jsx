import { Outlet } from "react-router-dom";

function Layout() {
  return (
    <div>
      <h2>블로그</h2>
      <Outlet />
    </div>
  );
}

export default Layout;
