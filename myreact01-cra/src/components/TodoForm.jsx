import { Form } from "react-bootstrap";

function TodoForm({ onEnter }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    const text = e.target.content.value.trim();
    // setTodoList((prev) => [...prev, { text, done: false }]);
    if (onEnter) {
      onEnter(text);
    }
    e.target.reset();
  };

  return (
    <Form onSubmit={(e) => handleSubmit(e)}>
      <Form.Control type="text" name="content" autoComplete="off" />
    </Form>
  );
}

export default TodoForm;
