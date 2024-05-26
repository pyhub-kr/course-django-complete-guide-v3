import { createBrowserRouter, Outlet, RouterProvider } from "react-router-dom";
import { Container } from "react-bootstrap";

// import "./App8.css";
import TopNav from "./components/TopNav";
import Footer from "./components/Footer";
import BlogLayout from "./pages/blog/Layout";
import BlogIndexPage from "./pages/blog/IndexPage";
import BlogPostDetailPage from "./pages/blog/PostDetailPage";
import RouterErrorPage from "./pages/RouterErrorPage";
import TodoList from "./pages/todos/TodoList";
import { StatusProvider } from "./contexts/StatusContext";

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
    errorElement: <RouterErrorPage />,
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
      { path: "todos", element: <TodoList /> },
    ],
  },
]);

function App() {
  return (
    <StatusProvider>
      <RouterProvider router={router} />
    </StatusProvider>
  );
}

export default App;
