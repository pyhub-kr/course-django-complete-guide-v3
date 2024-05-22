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
    <form onSubmit={(e) => handleSubmit(e)}>
      <input type="text" name="content" autoComplete="off" />
    </form>
  );
}

export default TodoForm;
