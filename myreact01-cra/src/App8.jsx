import { createBrowserRouter, Outlet, RouterProvider } from "react-router-dom";
import { Container } from "react-bootstrap";

// import "./App8.css";
import TopNav from "./components/TopNav";
import Footer from "./components/Footer";

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <>
        <TopNav />
        <Container>
          <Outlet />
          <hr />
          <Footer />
        </Container>
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
  return <RouterProvider router={router} />;
}

export default App;
