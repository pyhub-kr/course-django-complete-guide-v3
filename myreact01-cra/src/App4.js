function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

function App() {
  return (
    <div>
      <button onClick={() => console.log("clicked element")}>
        엘리먼트 버튼
      </button>
      <Button onClick={() => console.log("clicked component")}>
        컴포넌트 버튼
      </Button>
    </div>
  );
}

export default App;
