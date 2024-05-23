import { NavLink } from "react-router-dom";
import { Alert, Container, Nav, Navbar, NavDropdown } from "react-bootstrap";
import { useApiAxios } from "../api";

function TopNav() {
  const [{ data: whoamiHtml = null }] = useApiAxios({
    url: "/blog/whoami/",
    headers: {
      "Content-Type": "text/html",
    },
    // withCredentials: true,
  });

  console.log(whoamiHtml);

  return (
    <>
      <Navbar expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand to={"/"} as={NavLink}>
            파이썬 사랑방
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto" variant="underline">
              <Nav.Link to="/blog" as={NavLink}>
                블로그
              </Nav.Link>
              <Nav.Link to="/about" as={NavLink}>
                소개
              </Nav.Link>
              <NavDropdown title="계정" id="basic-nav-dropdown">
                <NavDropdown.Item to="/accounts/login" as={NavLink}>
                  로그인
                </NavDropdown.Item>
                <NavDropdown.Item to="/accounts/signup" as={NavLink}>
                  회원가입
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item to="/accounts/profile" as={NavLink}>
                  프로필
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item to="/accounts/logout" as={NavLink}>
                  로그아웃
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {whoamiHtml && (
        <Container>
          <Alert variant="info" className="mt-2">
            <div dangerouslySetInnerHTML={{ __html: whoamiHtml }} />
          </Alert>
        </Container>
      )}
    </>
  );
}

export default TopNav;
