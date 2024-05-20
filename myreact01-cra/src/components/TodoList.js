import { useState } from "react";

const INITIAL_TODO_LIST = [
  { text: "파이썬 익히기", done: true },
  { text: "장고 익히기", done: false },
];

const DONE_STYLE = { textDecoration: "line-through" };

function TodoList() {
  const [todoList, setTodoList] = useState(INITIAL_TODO_LIST);

  return (
    <div>
      <h2>할일 목록</h2>

      {todoList.map((todo) => {
        return (
          <li style={{ cursor: "pointer", ...(todo.done ? DONE_STYLE : null) }}>
            {todo.text}
          </li>
        );
      })}
    </div>
  );
}

export default TodoList;
