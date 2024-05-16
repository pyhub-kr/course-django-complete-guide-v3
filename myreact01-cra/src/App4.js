import TextInput from "./components/TextInput";

import Profile from "./components/Profile";
import Message from "./components/Message";
import { Button } from "react-bootstrap";

import "bootstrap/dist/css/bootstrap.min.css";

// function Button({ onClick, children }) {
//   return <button onClick={onClick}>{children}</button>;
// }

function App() {
  const handleClick = () => {
    console.log("clicked");
  };

  return (
    <div>
      <Button>bootstrap 버튼</Button>
      <div style={{ display: "flex", gap: "10px", margin: "10px" }}>
        <Message />
        <Profile />
      </div>

      <TextInput name={"username"} />
      <TextInput name={"email"} />
      {/*<button onClick={() => handleClick()}>엘리먼트 버튼</button>*/}
      {/*<Button onClick={() => console.log("clicked component")}>*/}
      {/*  컴포넌트 버튼*/}
      {/*</Button>*/}
    </div>
  );
}

export default App;
