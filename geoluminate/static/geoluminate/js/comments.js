$(".comment-flag").on('click', function(e) {
  //Triggers a modal that allows users to flag a comment for moderation
  var next = $(this).data('next')
  var action = $(this).data('action')
  var body = $(this).parents('.comment-body')
  var comment = body.find('.comment-content')
  var header = body.find('.comment-header :header')

  $('#flagComment_id').val(next)
  $('#flagCommentForm').attr('action',action)
  $('#flagCommentModal blockquote').html(comment.html())
  $('#flagCommentModal figcaption').html(header.html())
});

$(".comment-delete").on('click', function(e) {
  //Triggers a modal that allows moderators to remove a comment

  var next = $(this).data('next')
  var action = $(this).data('action')
  var body = $(this).parents('.comment-body')
  var comment = body.find('.comment-content')
  var header = body.find('.comment-header :header')

  $('#deleteComment_id').val(next)
  $('#deleteCommentForm').attr('action',action)
  $('#deleteCommentModal blockquote').html(comment.html())
  $('#deleteCommentModal figcaption').html(header.html())
});


$(".comment-reply").on('click', function(e) {
  // allows the user to open a comment form beneath an existing comment in order to directly reply to another user
  var next = $(this).data('next')
  var body = $(this).closest('.comment-wrapper')
  var reply_to = $(this).data('reply-to')

  var form = $('#commentForm')
  form.find('#id_next').val(next)
  form.find('#id_reply_to').val(reply_to)

  var $replies = body.find('.comment-replies')
  var $drawer = $replies.find('.comment-drawer').first()

  if ($drawer.is(':empty')){
    //clicked element contains no html

    //empty all drawers on page
    $('.comment-drawer').empty()

    //append form to current drawer
    $drawer.append(form.prop('outerHTML'))
    $replies.removeClass('hidden')


  } else {
    //a form is already in the drawer and the user wants to close it
    //simply empty all drawers
    $('.comment-drawer').empty()
  }

  

});