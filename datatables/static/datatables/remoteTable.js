var options = {};

function get_scrollY() {
  return $('.table-responsive').height() - (
    $('.dataTables_wrapper :first-child').height() + $('.dataTables_wrapper :last-child').height()
  )
}

function get_properties(url) {
  $.ajax({
    async: false,
    url: url,
    method: 'OPTIONS',
    success: function (data) {
      options = data;
      // $(data.data).each(function () {
      //   if (fields == null || fields.includes(this.key)) {
      //     column_props.push({
      //       title: this.ui.label,
      //       // title: this.key,
      //       data: this.key
      //     })
      //   }
      // })
    }
  });
  return options
}



$.fn.RemoteDataTable = function (url) {
  this.DataTable({
    ...get_properties(url),
    serverSide: true,
    // scrollY: get_scrollY(),
    ajax: {
      url: url,
      data: {
        format: 'datatables',
      },
    }
  })
  return this;
};

$.extend($.fn.dataTable.defaults, {
  // dom: '<"top"ipl>rt<"bottom"p><"clear">',
  // ordering: true,
  // searchable: false,
  // responsive: true,
  // processing: true,
  serverSide: true,
  // pageLength: 100,
  // hides the length menu and paginator if number of data don't exceed max page rows
  // preDrawCallback: function (settings) {
  //   var api = new $.fn.dataTable.Api(settings);
  //   // hides paginator
  //   $(this)
  //     .closest('.dataTables_wrapper')
  //     .find('.dataTables_paginate')
  //     .toggle(api.page.info().pages > 1);

  //   // hides length menu
  //   $(this)
  //     .closest('.dataTables_wrapper')
  //     .find('.dataTables_length')
  //     .toggle(settings.aLengthMenu[0][0] != -1 && settings.aLengthMenu[0][0] < api.page.info().recordsTotal);
  // },
});