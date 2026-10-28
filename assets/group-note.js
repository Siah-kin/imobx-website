// Owner, 28 Oct 2026: the open-group note appears as a short window when someone taps a link to the IMOBX Telegram group,
// before they leave the site, instead of a line on the page. Without JavaScript the link opens directly (a noscript note shows).
(function () {
  var dialog = document.getElementById('group-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var go = dialog.querySelector('[data-go]');
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href^="https://t.me/+"]');
    if (!link || dialog.contains(link)) return;
    event.preventDefault();
    go.href = link.href;
    dialog.showModal();
    go.focus();
  });
  dialog.querySelector('[data-back]').addEventListener('click', function () { dialog.close(); });
  go.addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) { if (event.target === dialog) dialog.close(); });
})();
