import { createBrowserRouter, Outlet, RouterProvider } from "react-router-dom";
import { Container } from "react-bootstrap";

// import "./App8.css";
import TopNav from "./components/TopNav";
import Footer from "./components/Footer";
import BlogLayout from "./pages/blog/Layout";
import BlogIndexPage from "./pages/blog/IndexPage";
import BlogPostDetailPage from "./pages/blog/PostDetailPage";

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
      {
        path: "blog",
        element: <BlogLayout />,
        children: [
          { index: true, element: <BlogIndexPage /> },
          { path: ":postId", element: <BlogPostDetailPage /> },
        ],
      },
      { path: "about", element: <div>About</div> },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
