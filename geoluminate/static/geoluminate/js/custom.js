$(function () {

  const $sidebar = $('#application-sidebar');
  var sidebarIsOpen = $sidebar.hasClass('expanded');
  const $nav = $('.navbar');

  function toggleSideBar() {
    if (sidebarIsOpen) {
      $sidebar.removeClass('expanded');
      return false
    } else {
      $sidebar.addClass('expanded');
      return true
    }
  }

  $('.toggle').on('click', function () {
    sidebarIsOpen = toggleSideBar()
  })

  $('.expand').on('click', function () {

    if ($nav.is(":visible")) {
      $nav.hide();
      $sidebar.removeClass('expanded')
    } else {
      $nav.show();
      if (sidebarIsOpen) {
        $sidebar.addClass('expanded')
      }
    }
  })

  $('#emailActionsForm').change(function (e) {
    e.preventDefault();
    var form = $(this);
    var formData = form.serializeArray();
    formData.push({
      name: 'action_primary',
      value: ''
    });
    $.post({
      url: form.attr('action'),
      data: formData,
      success: function (data) {
        location.href = '/';
        window.location.reload(true);
      },
      error: function (data) {
        form.replaceWith(data.responseJSON.form)
      },
    });
  });

  $("#addEmailForm").on('submit', function (e) {
    e.preventDefault();
    var form = $(this);
    var formData = form.serializeArray();
    formData.push({
      name: 'action_add',
      value: ''
    });

    $.post({
      url: form.attr('action'),
      data: formData,
      success: function (data) {
        location.href = '/';
        window.location.reload(true);
      },
      error: function (data) {
        form.replaceWith(data.responseJSON.form)
      },
    });
  });

  $('.removeEmail').on('click', function (e) {

    e.preventDefault();

    var formData = [{
        name: 'email',
        value: this.value
      },
      {
        name: this.name,
        value: ''
      }
    ];

    $.post({
      url: $('#emailActionsForm').attr('action'),
      data: formData,
      success: function (data) {
        location.href = '/';
        window.location.reload(true);
      },
      error: function (data) {
        location.href = '/';
        window.location.reload(true);
      },
    });
  });

  $('[data-bs-toggle="tooltip"]').tooltip()

  $('#glossaryFilter').on('keyup', function () {
    $('.definition').hide()
    $(`.definition:contains(${$(this).val()})`).show()
  })


});


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
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});