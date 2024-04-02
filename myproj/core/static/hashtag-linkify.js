(function() {
  observeNodeInsertion("[data-hashtag-linkify]", el => {
    const link = el.getAttribute("data-hashtag-linkify") || "";
    let html = el.innerHTML;
    const replacement = `<a href="${link}$1">#$1</a>`;
    html = html.replace(/#([\wㄱ-힣]+)/g, replacement);
    el.innerHTML = html;
  });
})();