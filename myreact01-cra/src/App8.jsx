import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  { path: "", element: <div>Home</div> },
  { path: "blog", element: <div>Blog</div> },
  { path: "about", element: <div>About</div> },
]);

function App() {
  return (
    <div>
      <h2>라우터</h2>
      <ul>
        <li>
          <a href="/">홈</a>
        </li>
        <li>
          <a href="/blog">블로그</a>
        </li>
        <li>
          <a href="/about">소개</a>
        </li>
      </ul>
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
