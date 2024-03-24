document.body.addEventListener('htmx:configRequest', function (event) {
  const htmxElement = event.detail.elt;
  const isGetRequest = htmxElement.hasAttribute('hx-get');
  if (isGetRequest && htmxElement.hasAttribute('hx-get-with-timestamp')) {
    const paramName = htmxElement.getAttribute('hx-get-with-timestamp') || '_';
    event.detail.parameters[paramName] = new Date().getTime();
  }
});
