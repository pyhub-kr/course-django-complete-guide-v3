function Button({ onClick }) {
  return <button onClick={onClick}>컴포넌트 버튼</button>;
}

function App() {
  return (
    <div>
      <button onClick={() => console.log("clicked element")}>
        엘리먼트 버튼
      </button>
      <Button onClick={() => console.log("clicked component")} />
    </div>
  );
}

export default App;
