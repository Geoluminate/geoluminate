function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

$(function() {
  if (!$('#feedback-btn').length) {
      var $btn = $("{% filter escapejs %}{% include 'tellme/tpl-button.html' %}{% endfilter %}");
      $('body').append($btn);
      if (!$('#feedback-btn').length) {
          $btn.attr('id', 'feedback-btn');
      }
  }




//   $.feedback({
//       ajaxURL: "{% url 'tellme:post_feedback' %}",
//       html2canvasURL: "{% block html2canvasURL %}{% static 'tellme/vendor/html2canvas/html2canvas.js' %}{%  endblock %}",
//       feedbackButton: "#feedback-btn",
//       initButtonText: "{% filter escapejs %}{%  include 'tellme/initButtonText.txt' %}{% endfilter %}",
//       postHTML: false,
//       tpl: {
//           description: "{% filter escapejs %}{%  include 'tellme/tpl-description.html' %}{% endfilter %}",
//           highlighter: "{% filter escapejs %}{%  include 'tellme/tpl-highlighter.html' %}{% endfilter %}",
//           overview: "{% filter escapejs %}{%  include 'tellme/tpl-overview.html' %}{% endfilter %}",
//           submitSuccess: "{% filter escapejs %}{%  include 'tellme/tpl-submit-success.html' %}{% endfilter %}",
//           submitError: "{% filter escapejs %}{%  include 'tellme/tpl-submit-error.html' %}{% endfilter %}"
//       },
//       initialBox: true
//   });
});