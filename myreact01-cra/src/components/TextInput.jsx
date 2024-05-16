import { useState } from "react";
import PropTypes from "prop-types";

function TextInput({ name }) {
  const [length, setLength] = useState(0);

  const handleTextChange = (currentText) => {
    setLength(currentText.length);
  };

  return (
    <div>
      <input
        type="text"
        name={name}
        autoComplete={"off"}
        onChange={(e) => {
          console.log("changed", e.target.value);
          handleTextChange(e.target.value);
        }}
      />
      <div>
        <small>입력 글자 수 : {length}</small>
      </div>
    </div>
  );
}

TextInput.propTypes = {
  name: PropTypes.string.isRequired,
};

export default TextInput;
