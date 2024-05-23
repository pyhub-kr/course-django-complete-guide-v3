import {createRoot} from "react-dom/client";

class BaseComponent extends HTMLElement {
  constructor() {
    super();
    this.root = createRoot(this);
    this.props = {self: this};
  }

  // 컴포넌트 생성 시에 모든 속성을 props에 저장하고, 컴포넌트를 렌더링합니다.
  connectedCallback() {
    BaseComponent.observedAttributes.reduce((acc, attr_name) => {
      const prop_name = attr_name.replace(/^data-/, "");  // 이름에서 data- 접두사를 제거합니다.
      acc[prop_name] = this.getAttribute(attr_name);
      return acc;
    }, this.props);

    this.updateComponent();
  }

  disconnectedCallback() {
    this.root.unmount();
  }

  // 속성값이 변경되었을 때 this.props에 반영하고 컴포넌트를 재렌더링합니다.
  attributeChangedCallback(attr_name, oldValue, newValue) {
    if (oldValue !== newValue) {
      const prop_name = attr_name.replace(/^data-/, "");  // 이름에서 data- 접두사를 제거합니다.
      this.props[prop_name] = newValue;
      this.updateComponent();
    }
  }

  // 속성값에서 null인 값은 제거하고 컴포넌트를 재렌더링합니다.
  updateComponent() {
    // null인 값은 제거합니다.
    this.props = Object.entries(this.props).reduce((acc, [key, value]) => {
      if (value !== null) acc[key] = value;
      return acc;
    }, {});

    this.render(this.props);
  }

  // 리액트 컴포넌트를 재렌더링하는 메서드입니다. 자식 컴포넌트에서 필히 구현해야 합니다.
  render(props) {
    throw new Error("리액트 컴포넌트 재렌더링 메서드를 구현해야 합니다.")
  }

  // 자식 컴포넌트에서 지원할 속성명을 배열로 반환합니다.
  static get observedAttributes() {
    return [];
  }
}

export default BaseComponent;
