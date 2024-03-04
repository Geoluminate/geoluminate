// import $ from 'jquery'


// $('#emailActionsForm').on('change', function (e) {
//   e.preventDefault()
//   var form = $(this)
//   var formData = form.serializeArray()
//   formData.push({
//     name: 'action_primary',
//     value: ''
//   })
//   $.post({
//     url: form.attr('action'),
//     data: formData,
//     success: function (data) {
//       location.href = '/'
//       window.location.reload()
//     },
//     error: function (data) {
//       form.replaceWith(data.responseJSON.form)
//     },
//   })
// })

// $("#addEmailForm").on('submit', function (e) {
//   e.preventDefault()
//   var form = $(this)
//   var formData = form.serializeArray()
//   formData.push({
//     name: 'action_add',
//     value: ''
//   })

//   $.post({
//     url: form.attr('action'),
//     data: formData,
//     success: function (data) {
//       location.href = '/'
//       window.location.reload()
//     },
//     error: function (data) {
//       form.replaceWith(data.responseJSON.form)
//     },
//   })
// })

// $('.removeEmail').on('click', function (e) {

//   e.preventDefault()

//   var formData = [{
//     name: 'email',
//     value: this.value
//   },
//   {
//     name: this.name,
//     value: ''
//   }
//   ]

//   $.post({
//     url: $('#emailActionsForm').attr('action'),
//     data: formData,
//     success: function (data) {
//       location.href = '/'
//       window.location.reload()
//     },
//     error: function (data) {
//       location.href = '/'
//       window.location.reload()
//     },
//   })
// })
