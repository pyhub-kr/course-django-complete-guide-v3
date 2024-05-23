import BaseComponent from "./base";
import * as styles from "./hello_world.module.css";
import { useEffect, useState } from "react";

function HelloWorld({ self, name = "익명" }) {
  const [count, setCount] = useState(0);
  const [color, setColor] = useState("yellow");

  useEffect(() => {
    const newColor = count % 2 === 0 ? "green" : "red";
    setColor(newColor);
    self.dispatchEvent(new CustomEvent("color-changed", { detail: newColor }));
  }, [count]);

  return (
    <div className={styles.container} style={{ color: color }}>
      <h1>Hello, {name}</h1>
      <button onClick={() => setCount((prev) => prev + 1)}>+1</button>
    </div>
  );
}

class HelloWorldComponent extends BaseComponent {
  // 인자로 전달받은 속성값으로 리액트 컴포넌트를 렌더링합니다.
  render(props) {
    this.root.render(<HelloWorld {...props} />);
  }

  // 지원할 속성명을 배열로 반환합니다.
  static get observedAttributes() {
    return ["data-name"];
  }
}

customElements.define("hello-world", HelloWorldComponent);
