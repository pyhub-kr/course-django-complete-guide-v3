/* components/src-django-components/hello_world/hello_world.js */
/*  - 각 컴포넌트마다 반복되는 것이 아니라, 웹페이지에서 1회만 수행 */

(function () {
  document.querySelectorAll(".hello-world-component h1").forEach(el => {
    el.onclick = function (e) {
      alert(e.target.textContent);
    };
  });
})()
