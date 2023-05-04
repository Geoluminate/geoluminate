if (!$) {
  $ = django.jQuery;
}

$(function () {

  const $select = $('.select2');

  $select.select2({
    multiple: true,
    tags: true,


  });

})