import {useState} from "react";

function Counter({ initialCount }) {
  const [count, setCount] = useState(initialCount);

  return (
    <button onClick={() => setCount(count + 1)}>{count}</button>
  )
}

function App() {
  const style = {margin: "1em"};

  return (
    <div className={"App"} style={style}>
      <Counter initialCount={10} />
      <Counter initialCount={20} />
      <Counter initialCount={30} />
    </div>
  );
}

export default App;
