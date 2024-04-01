/*
 * https://getbootstrap.com/docs/5.3/components/carousel/#how-it-works
 *
 * 성능상의 이유로 캐로셀은 Carousel 생성자 메서드를 통해 수동으로 초기화되어야만 합니다.
 * 그렇지 않으면, 터치/스와이프 지원이 필요한 일부 이벤트 리스너들은 명시적으로 활성화하기 전까지는 등록되지 않습니다.
 * 예) 두번째 페이지부터 swipe가 동작
 * For performance reasons, carousels must be manually initialized using the carousel constructor method.
 * Without initialization, some of the event listeners (specifically, the events needed touch/swipe support) will
 * not be registered until a user has explicitly activated a control or indicator.
 */

(function() {
  observeNodeInsertion(".carousel-component", carouselEl => {
    const carousel = new bootstrap.Carousel(carouselEl);

    /* Desktop에서는 swipe가 동작하지 않아서, 직접 swipe 구현 */

    let mouseStartX = 0;
    carouselEl.addEventListener("mousedown", (e) => {
      mouseStartX = e.screenX;
      document.body.style.cursor = 'grabbing';
    });

    carouselEl.addEventListener("mouseup", (e) => {
      const mouseEndX = e.screenX;
      if(mouseStartX < mouseEndX) carousel.next();
      else carousel.prev();
      document.body.style.cursor = 'default';
    });
  });
})();
