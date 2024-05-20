import { useReducer, useState } from "react";
import { produce } from "immer";

const INITIAL_STATE = {
  count: 0,
  color: "green",
};

function reducer(currentState, action) {
  return produce(currentState, (draft) => {
    const { type } = action;

    if (type === "plus") {
      draft.count += 1;
    } else if (type === "minus") {
      draft.count -= 1;
    }

    draft.color = draft.count % 2 === 0 ? "green" : "red";
  });
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, INITIAL_STATE);

  const increment = () => {
    const action = { type: "plus" };
    dispatch(action);
    // setState(
    //   produce((draft) => {
    //     draft.count += 1;
    //     draft.color = draft.count % 2 === 0 ? "green" : "red";
    //   }),
    // );
  };
  const decrement = () => {
    const action = { type: "minus" };
    dispatch(action);
    // setState(
    //   produce((draft) => {
    //     draft.count -= 1;
    //     draft.color = draft.count % 2 === 0 ? "green" : "red";
    //   }),
    // );
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
