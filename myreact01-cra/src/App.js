import { useState } from "react";

function Counter({ initialCount }) {
  const [count, setCount] = useState(initialCount);

  const increment = () => {
    // setCount(count + 1);
    // setCount(count + 1);
    setCount((prevCount) => prevCount + 1);
    setCount((prevCount) => prevCount + 1);
  };

  const decrement = () => {
    setCount((prevCount) => prevCount - 1);
  };

  return (
    <button
      onClick={() => increment()}
      onContextMenu={(e) => {
        e.preventDefault();
        decrement();
      }}
    >
      {count}
    </button>
  );
}

function App() {
  const style = { margin: "1em" };

  return (
    <div className={"App"} style={style}>
      <Counter initialCount={10} />
      <Counter initialCount={20} />
      <Counter initialCount={30} />
    </div>
  );
}

export default App;
