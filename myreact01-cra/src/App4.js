import TextInput from "./components/TextInput";

import Profile from "./components/Profile";
import Message from "./components/Message";

function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

function App() {
  const handleClick = () => {
    console.log("clicked");
  };

  return (
    <div>
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
