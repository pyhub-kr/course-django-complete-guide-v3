import React, { useState } from "react";
import { produce } from "immer";
import TodoForm from "../../components/TodoForm";
import { Button, Card, Container, ListGroup, Spinner } from "react-bootstrap";
import { makeRestApi, useApiAxios } from "../../api";

const DONE_STYLE = { textDecoration: "line-through" };

const TODO_REST_API = makeRestApi("/blog/api/todos/");

function TodoList() {
  const [{ data: todoList = [], loading, error: loadingError }, refetch] =
    useApiAxios("/blog/api/todos/");

  const toggleTodo = async (todoIndex) => {
    console.log(`인덱스#${todoIndex}를 토글합니다.`);

    const todo = todoList[todoIndex];
    const { data, error } = await TODO_REST_API.update(todo.id, {
      done: !todo.done,
    });
    console.log("응답 데이터 :", data);
    refetch();

    // setTodoList(
    //   produce((draftTodoList) => {
    //     draftTodoList[todoIndex].done = !draftTodoList[todoIndex].done;
    //   }),
    // );
  };

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //
  //   const text = e.target.content.value.trim();
  //   setTodoList((prev) => [...prev, { text, done: false }]);
  //   e.target.reset();
  // };

  const addTodo = (newText) => {
    // setTodoList((prev) => [...prev, { text: newText, done: false }]);
  };

  const deleteTodo = (todoIndex) => {
    if (window.confirm("정말 삭제하시겠습니까?")) {
      // setTodoList((prev) => {
      //   return prev.filter((_, index) => index !== todoIndex);
      // });
    }
  };

  const editTodo = (todoIndex) => {
    const todo = todoList[todoIndex];
    const origText = todo.text;
    const promptText = window.prompt("수정할 내용을 입력하세요.", origText);
    if (promptText !== null && promptText !== origText) {
      // setTodoList(
      //   produce((draftTodoList) => {
      //     draftTodoList[todoIndex].text = promptText;
      //   }),
      // );
    }
  };

  return (
    <Container>
      <Card>
        <Card.Header>
          할일 목록
          {loading && (
            <Spinner
              animation="grow"
              variant="primary"
              size="sm"
              className="mx-1"
            />
          )}
        </Card.Header>

        <ListGroup variant="flush">
          {loadingError && (
            <ListGroup.Item variant="danger">
              {loadingError.message}
            </ListGroup.Item>
          )}

          {todoList.length === 0 && (
            <ListGroup.Item variant="warning">
              등록된 할일이 없습니다.
            </ListGroup.Item>
          )}

          {todoList.map((todo, index) => {
            return (
              <ListGroup.Item
                key={index}
                className="d-flex justify-content-between align-items-start"
              >
                <div
                  style={{
                    cursor: "pointer",
                    ...(todo.done ? DONE_STYLE : null),
                  }}
                  onClick={() => toggleTodo(index)}
                >
                  {todo.text}
                </div>
                <div>
                  <Button
                    variant="outline-primary"
                    size="sm"
                    className="me-1"
                    onClick={() => editTodo(index)}
                  >
                    수정
                  </Button>
                  <Button
                    variant="outline-danger"
                    size="sm"
                    onClick={() => deleteTodo(index)}
                  >
                    삭제
                  </Button>
                </div>
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
