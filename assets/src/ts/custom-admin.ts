import $ from 'jquery'
import "./ajax"

$(function () {
  if (!$('#feedback-btn').length) {
    var $btn = $("{% filter escapejs %}{% include 'tellme/tpl-button.html' %}{% endfilter %}")
    $('body').append($btn)
    if (!$('#feedback-btn').length) {
      $btn.attr('id', 'feedback-btn')
    }
  }
})
