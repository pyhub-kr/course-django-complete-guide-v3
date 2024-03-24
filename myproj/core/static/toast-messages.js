(function () {
  function getColorClass(tag) {
    return {
      "info": "text-white bg-primary",
      "success": "text-white bg-success",
      "warning": "text-dark bg-warning",
      "error": "text-white bg-danger",
      "debug": "text-white bg-secondary",
    }[tag] || "text-white bg-secondary";
  }

  function getButtonClass(tag) {
    return {
      "warning": "btn-close-dark",
      "debug": "btn-close-dark",
    }[tag] || "btn-close-white";
  }

  const html = `<div class="toast-container position-fixed top-0 end-0 p-3"></div>`
  document.body.insertAdjacentHTML('beforeend', html);

  /* body 요소에서 toast-message 이벤트를 처리합니다. */
  document.body.addEventListener("toast-message", function (e) {
    const {message, tag} = e.detail;
    const colorClass = getColorClass(tag);
    const buttonClass = getButtonClass(tag);

    const html = `
      <div class="toast align-items-center border-0 ${colorClass}" data-bs-autohide="true">
          <div class="d-flex">
              <div class="toast-body">${message}</div>
              <button type="button" class="btn-close me-2 m-auto ${buttonClass}" data-bs-dismiss="toast"></button>
          </div>
      </div>
  `;

    const container = document.querySelector(".toast-container");
    container.insertAdjacentHTML('afterbegin', html);

    const toastEl = container.querySelector('.toast:first-child');
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  });
})();