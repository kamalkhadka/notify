$(function () {
  if (window.location.href.endsWith("/messages")) {
    CKEDITOR.replace("message");
  }

  $('.toast').toast('show');
});
