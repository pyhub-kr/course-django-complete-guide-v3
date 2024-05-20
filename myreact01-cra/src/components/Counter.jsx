import { useState } from "react";
import { produce } from "immer";

function Counter() {
  const [state, setState] = useState({
    count: 0,
    color: "green",
  });

  const increment = () => {
    setState(
      produce((draft) => {
        draft.count += 1;
        draft.color = draft.count % 2 === 0 ? "green" : "red";
      }),
    );
  };
  const decrement = () => {
    setState(
      produce((draft) => {
        draft.count -= 1;
        draft.color = draft.count % 2 === 0 ? "green" : "red";
      }),
    );
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h1 style={{ color: state.color }}>{state.count}</h1>
      <button onClick={() => increment()}>+1</button>
      <button onClick={() => decrement()}>-1</button>
    </div>
  );
}

export default Counter;
