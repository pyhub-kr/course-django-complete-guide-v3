(function () {
  observeNodeInsertion(".modal-form-component", (modalEl) => {
    let modal = bootstrap.Modal.getInstance(modalEl);
    if(modal) return;

    modal = new bootstrap.Modal(modalEl);
    modal.show();

    const submitButtonEl = modalEl.querySelector("button[type=submit]");
    if (submitButtonEl) {
      // 저장 버튼을 클릭하면, form submit 이벤트를 발생시킵니다.
      submitButtonEl.onclick = () => {
        const formEl = modalEl.querySelector("form");
        if (formEl) {
          if (window.htmx) htmx.trigger(formEl, "submit");
          else formEl.dispatchEvent(new CustomEvent("submit"));
        }
      };
    }
    else {
      console.warn("not found submit button.");
    }

    modalEl.addEventListener("hide", () => {
      modal.hide();
    });
  });
})();