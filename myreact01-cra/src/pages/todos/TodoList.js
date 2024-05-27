import React, { useEffect, useState } from "react";
import { produce } from "immer";
import TodoForm from "../../components/TodoForm";
import { Button, Card, Container, ListGroup, Spinner } from "react-bootstrap";
import { makeRestApi, useApiAxios } from "../../api";
import IFrameModal from "../../components/IFrameModal";

const DONE_STYLE = { textDecoration: "line-through" };

const TODO_REST_API = makeRestApi("/blog/api/todos/");

function TodoList() {
  const [
    { data: origTodoList = undefined, loading, error: loadingError },
    refetch,
  ] = useApiAxios("/blog/api/todos/");

  const [todoList, setTodoList] = useState([]);
  const [iframeSrc, setIframeSrc] = useState(null);

  useEffect(() => {
    setTodoList(origTodoList || []);
  }, [origTodoList]);

  const toggleTodo = async (todoIndex) => {
    console.log(`인덱스#${todoIndex}를 토글합니다.`);

    const todo = todoList[todoIndex];
    const { data, error } = await TODO_REST_API.update(todo.id, {
      done: !todo.done,
    });
    if (data) {
      const editedTodo = data;

      setTodoList(
        produce((draftTodoList) => {
          draftTodoList[todoIndex] = editedTodo;
        }),
      );
    }
  };

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //
  //   const text = e.target.content.value.trim();
  //   setTodoList((prev) => [...prev, { text, done: false }]);
  //   e.target.reset();
  // };

  const addTodo = async (newText) => {
    const { data, error } = await TODO_REST_API.create({ text: newText });
    if (data) {
      const newTodo = data;
      setTodoList((prev) => [...prev, newTodo]);
    }
  };

  const deleteTodo = async (todoIndex) => {
    if (window.confirm("정말 삭제하시겠습니까?")) {
      const todo = todoList[todoIndex];
      const { data, response } = await TODO_REST_API.delete(todo.id);
      if (response?.status === 204) {
        setTodoList((prev) => {
          return prev.filter((_, index) => index !== todoIndex);
        });
      }
    }
  };

  const editTodo = async (todoIndex) => {
    const todo = todoList[todoIndex];
    setIframeSrc(`/blog/todos/${todo.id}/edit/`);

    // const origText = todo.text;
    // const promptText = window.prompt("수정할 내용을 입력하세요.", origText);
    // if (promptText !== null && promptText !== origText) {
    //   const { data, error } = await TODO_REST_API.update(todo.id, {
    //     text: promptText,
    //   });
    //   if (data) {
    //     setTodoList(
    //       produce((draftTodoList) => {
    //         draftTodoList[todoIndex] = data;
    //       }),
    //     );
    //   }
    // }
  };

  return (
    <Container>
      {!!iframeSrc && (
        <IFrameModal
          title="할일"
          handleClose={(currentTodo) => {
            // if (currentTodo) setTodoList((prev) => [...prev, currentTodo]);
            if (currentTodo) {
              setTodoList(
                produce((draft) => {
                  const todoIndex = draft.findIndex(
                    (todo) => todo.id === currentTodo.id,
                  );
                  if (todoIndex !== -1) {
                    draft[todoIndex] = currentTodo;
                  } else {
                    draft.push(currentTodo);
                  }
                }),
              );
            }
            setIframeSrc(null);
          }}
          iframeSrc={iframeSrc}
        />
      )}

      <Card>
        <Card.Header className="d-flex align-items-center">
          할일 목록
          {loading && (
            <Spinner
              animation="grow"
              variant="primary"
              size="sm"
              className="mx-1"
            />
          )}
          <Button
            className="ms-auto"
            size="sm"
            onClick={() => setIframeSrc("/blog/todos/new/")}
          >
            새 할일
          </Button>
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
