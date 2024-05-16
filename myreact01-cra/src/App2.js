import { createContext, useContext, useState } from "react";

function App() {
  return <Root />;
}

const CountContext = createContext();

function Root() {
  const [count, setCount] = useState(0);

  const increment = () => setCount((prev) => prev + 1);

  return (
    <CountContext.Provider value={{ count }}>
      <div>
        <button onClick={() => increment()}>증가</button>
        <A />
        <B />
      </div>
    </CountContext.Provider>
  );
}

function A() {
  return <div>A 컴포넌트</div>;
}

function B() {
  return (
    <div>
      B 컴포넌트
      <C />
    </div>
  );
}

function C() {
  return (
    <div>
      C 컴포넌트
      <D />
      <E />
    </div>
  );
}

function D() {
  return <div>D 컴포넌트</div>;
}

function E() {
  return (
    <div>
      E 컴포넌트
      <Leaf />
    </div>
  );
}

function Leaf() {
  const { count } = useContext(CountContext);
  return <div>말단 컴포넌트: {count}</div>;
}

export default App;
