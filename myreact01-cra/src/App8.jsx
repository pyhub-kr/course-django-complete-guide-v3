import {
  createBrowserRouter,
  NavLink,
  Outlet,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <>
        <ul>
          <li>
            <NavLink to="/">홈</NavLink>
          </li>
          <li>
            <NavLink to="/blog">블로그</NavLink>
          </li>
          <li>
            <NavLink to="/about">소개</NavLink>
          </li>
        </ul>
        <Outlet />
      </>
    ),
    children: [
      { index: true, element: <div>Home</div> },
      { path: "blog", element: <div>Blog</div> },
      { path: "about", element: <div>About</div> },
    ],
  },
]);

function App() {
  return (
    <div>
      <h2>라우터</h2>
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
