import $ from 'jquery'
import * as utils from './utils'
import jszip from 'jszip';
import pdfmake from 'pdfmake';
import DataTable from 'datatables.net-bs5';
import "datatables.net-bs5/css/dataTables.bootstrap5.min.css";
import 'datatables.net-buttons-bs5';
import 'datatables.net-buttons/js/buttons.colVis.mjs';
import 'datatables.net-buttons/js/buttons.html5.mjs';
import 'datatables.net-buttons/js/buttons.print.mjs';
import 'datatables.net-colreorder-bs5';
import DateTime from 'datatables.net-datetime';
import 'datatables.net-fixedcolumns-bs5';
import 'datatables.net-fixedheader-bs5';
import 'datatables.net-keytable-bs5';
import 'datatables.net-responsive-bs5';
// import 'datatables.net-rowgroup-bs5';
// import 'datatables.net-rowreorder-bs5';
import 'datatables.net-scroller-bs5/css/scroller.bootstrap5.css';
import 'datatables.net-scroller-bs5';
import 'datatables.net-searchbuilder-bs5/css/searchBuilder.bootstrap5.css';
import 'datatables.net-searchbuilder-bs5';
import 'datatables.net-searchpanes-bs5/css/searchPanes.bootstrap5.css';
import 'datatables.net-searchpanes-bs5';
import 'datatables.net-select-bs5';
import 'datatables.net-staterestore-bs5';
import '../../styles/datatables.scss';
import { main } from '@popperjs/core'

DataTable.Buttons.defaults.dom.button.className = 'nav-link m-1';

Object.assign(DataTable.defaults, {
  dom: `<'page-nav'<'nav nav-pills nav-pills-alternate'B<'ms-auto my-auto'f>>>
            rt
        <'px-1 position-absolute bottom-0 end-0'i>`,
  searching: true,
  ordering: true,
});


$.fn.extend({
  AutoTable: function () {

    const config = utils.getTableConfig($(this));

    if (config.debug) {
      console.log($(this).data('ajax'))
      console.log(config)
    }

    // check is config.datatables.scroller is set and if it is, set the scrollY to the height of the table wrapper minus the height of the table
    if (config.datatables.scroller) {
      var height = $(".table-wrapper").height()
      var table_height = $(this).height()
      var scrollerHeight = height - table_height

      config.datatables.scrollY = scrollerHeight + "px"
      // config.datatables.scrollY = "200px"
    }


    // const metadata = config.metadata || []
    // const choiceFields = utils.getMetadataByType(metadata, "select");

    return $(this).DataTable({
      ...config.datatables,
      ajax: {
        url: $(this).data('ajax'),
        headers: {
          "Accept": 'application/datatables+json',
          "Content-Type": "text/json; charset=utf-8",
        },
      },
      columnDefs: [
        ...utils.buildColumnDefs(config),
      ],
      initComplete: function(settings, json) {
        $(this).addClass('loaded')
      },

     } );
  }
});
