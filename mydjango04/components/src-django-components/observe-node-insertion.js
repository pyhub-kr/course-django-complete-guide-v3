/* components/src-django-components/observe-node-insertion.js */

function observeNodeInsertion(selector, callback) {
  // 이미 존재하는 노드에 대한 처리
  document.querySelectorAll(selector).forEach(callback);

  // 새로 추가되는 노드에 대해서 탐지
  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.type === "childList") {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE && node.matches(selector)) {
            if (callback)
              callback(node);
          }
        }
      }
    }
  });
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
}
