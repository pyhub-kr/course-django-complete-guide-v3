import { useState } from "react";

function App() {
  return <Root />;
}

function Root() {
  const [count, setCount] = useState(0);

  const increment = () => setCount((prev) => prev + 1);

  return (
    <div>
      <button onClick={() => increment()}>증가</button>
      <A count={count} />
      <B count={count} />
    </div>
  );
}

function A({ count }) {
  return <div>A 컴포넌트</div>;
}

function B({ count }) {
  return (
    <div>
      B 컴포넌트
      <C count={count} />
    </div>
  );
}

function C({ count }) {
  return (
    <div>
      C 컴포넌트
      <D count={count} />
      <E count={count} />
    </div>
  );
}

function D({ count }) {
  return <div>D 컴포넌트</div>;
}

function E({ count }) {
  return (
    <div>
      E 컴포넌트
      <Leaf count={count} />
    </div>
  );
}

function Leaf({ count }) {
  return <div>말단 컴포넌트: {count}</div>;
}

export default App;
