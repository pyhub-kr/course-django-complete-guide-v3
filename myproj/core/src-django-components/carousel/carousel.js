(function () {
  observeNodeInsertion(".carousel-component", el => {
    const carousel = new bootstrap.Carousel(el);

    /* 비 touch 디바이스에서는 swipe가 동작하지 않아서, 직접 swipe 구현 */

    let mouseStartX = 0;
    let mouseStartY = 0;

    el.addEventListener("mousedown", e => {
      mouseStartX = e.screenX;
      mouseStartY = e.screenY;
      document.body.style.cursor = "grabbing";
    });

    el.addEventListener("mouseup", e => {
      const mouseEndX = e.screenX;
      const mouseEndY = e.screenY;

      const deltaX = Math.abs(mouseEndX - mouseStartX);
      const deltaY = Math.abs(mouseEndY - mouseStartY);

      if (deltaX > deltaY) {
        if(mouseStartX < mouseEndX) carousel.prev();
        else if (mouseStartX > mouseEndX) carousel.next();
      }

      document.body.style.cursor = "default";
    });
  });
})();