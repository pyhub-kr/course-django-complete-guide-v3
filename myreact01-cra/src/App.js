import { useState } from "react";

function Counter({ initialCount }) {
  const [count, setCount] = useState(() => {
    if (initialCount >= 10) return 10;
    if (initialCount <= 0) return 0;
    return initialCount;
  });

  const increment = () => {
    setCount((prevCount) => {
      if (prevCount >= 10) return 10;
      return prevCount + 1;
    });
  };

  const decrement = () => {
    setCount((prevCount) => {
      if (prevCount <= 0) return 0;
      return prevCount - 1;
    });
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
