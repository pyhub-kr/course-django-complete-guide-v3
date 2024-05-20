import { useState } from "react";

const INITIAL_TODO_LIST = [
  { text: "파이썬 익히기", done: true },
  { text: "장고 익히기", done: false },
];

const DONE_STYLE = { textDecoration: "line-through" };

function TodoList() {
  const [todoList, setTodoList] = useState(INITIAL_TODO_LIST);

  const toggleTodo = (todoIndex) => {
    console.log(`인덱스#${todoIndex}를 토글합니다.`);
    // todoList[todoIndex].done = !todoList[todoIndex].done;

    const newTodoList = todoList.map((todo, index) => {
      if (index === todoIndex) {
        return { ...todo, done: !todo.done };
      }
      return todo;
    });
    setTodoList(newTodoList);
  };

  return (
    <div>
      <h2>할일 목록</h2>

      {todoList.map((todo, index) => {
        return (
          <li
            key={index}
            style={{ cursor: "pointer", ...(todo.done ? DONE_STYLE : null) }}
            onClick={() => toggleTodo(index)}
          >
            {todo.text}
          </li>
        );
      })}
    </div>
  );
}

export default TodoList;
