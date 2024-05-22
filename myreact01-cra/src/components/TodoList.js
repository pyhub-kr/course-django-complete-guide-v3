import React, { useState } from "react";
import { produce } from "immer";
import TodoForm from "./TodoForm";
import { Card, Container, ListGroup } from "react-bootstrap";

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

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //
  //   const text = e.target.content.value.trim();
  //   setTodoList((prev) => [...prev, { text, done: false }]);
  //   e.target.reset();
  // };

  const addTodo = (newText) => {
    setTodoList((prev) => [...prev, { text: newText, done: false }]);
  };

  return (
    <Container>
      <Card>
        <Card.Header>할일 목록</Card.Header>

        <ListGroup variant="flush">
          {todoList.length === 0 && (
            <ListGroup.Item variant="warning">
              등록된 할일이 없습니다.
            </ListGroup.Item>
          )}

          {todoList.map((todo, index) => {
            return (
              <ListGroup.Item
                key={index}
                style={{
                  cursor: "pointer",
                  ...(todo.done ? DONE_STYLE : null),
                }}
                onClick={() => toggleTodo(index)}
              >
                {todo.text}
              </ListGroup.Item>
            );
          })}
        </ListGroup>

        <Card.Body>
          <TodoForm onEnter={(newText) => addTodo(newText)} />
        </Card.Body>
      </Card>
    </Container>
  );
}

export default TodoList;
