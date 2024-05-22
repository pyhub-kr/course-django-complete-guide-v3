import { useState } from "react";
import { produce } from "immer";

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

    // const newTodoList = todoList.map((todo, index) => {
    //   if (index === todoIndex) {
    //     return { ...todo, done: !todo.done };
    //   }
    //   return todo;
    // });
    // setTodoList(newTodoList);

    setTodoList(
      produce((draftTodoList) => {
        draftTodoList[todoIndex].done = !draftTodoList[todoIndex].done;
      }),
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const text = e.target.content.value.trim();
    setTodoList((prev) => [...prev, { text, done: false }]);
    e.target.reset();
  };

  return (
    <div>
      <h2>할일 목록</h2>

      {todoList.length === 0 && (
        <div style={{ color: "indianred" }}>등록된 할일이 없습니다.</div>
      )}

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

      <form onSubmit={(e) => handleSubmit(e)}>
        <input type="text" name="content" autoComplete="off" />
      </form>
    </div>
  );
}

export default TodoList;
