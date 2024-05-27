import { Alert, Modal } from "react-bootstrap";
import { useEffect, useState } from "react";
import { API_HOST } from "../constants";

function IFrameModal({ title, iframeSrc, handleClose }) {
  const [url, setUrl] = useState(null);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    let url = iframeSrc;
    if (url.startsWith("/")) {
      url = API_HOST + url;
    }
    setUrl(url);
  }, [iframeSrc]);

  useEffect(() => {
    const handleMessage = (event) => {
      if (url.startsWith(event.origin)) {
        if (event.data.event === "saved") {
          const savedData = event.data.data;
          if (handleClose) handleClose(savedData);
        }
        if (event.data.event === "resize") {
          const { height } = event.data;
          setHeight(height + 32); // padding 16px * 2
        }
      }
    };

    window.addEventListener("message", handleMessage);

    return () => {
      window.removeEventListener("message", handleMessage);
    };
  }, [url, handleClose]);

  return (
    <Modal
      show={true}
      onHide={() => handleClose && handleClose()}
      size={"lg"}
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title>{title || "no title"}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {!url && (
          <Alert variant="warning">iframeSrc 속성값을 지정해주세요.</Alert>
        )}
        {url && (
          <iframe
            src={url}
            width="100%"
            height={height}
            style={{ border: "none" }}
            title="iframe-content"
          ></iframe>
        )}
      </Modal.Body>
    </Modal>
  );
}

export default IFrameModal;
