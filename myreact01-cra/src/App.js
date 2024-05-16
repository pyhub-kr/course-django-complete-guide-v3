
function App() {
  const style = {margin: "1em"};
  const children = <h1>HELLO WORLD</h1>;

  return (
    <div className={"App"} style={style}>
      {children}
    </div>
  );
}

export default App;
