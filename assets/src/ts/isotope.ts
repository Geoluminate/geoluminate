import $ from 'jquery';
// import 'isotope-layout';
import "isotope-layout/dist/isotope.pkgd.min.js";

declare global {
  interface Window {
    $: any;
  }
}

// store filter for each group
var filters: any[] = [];

function addFilter( filter: string ) {
  if ( filters.indexOf( filter ) == -1 ) {
    filters.push( filter );
  }
}

function removeFilter( filter: string ) {
  var index = filters.indexOf( filter);
  if ( index != -1 ) {
    filters.splice( index, 1 );
  }
}


document.addEventListener("htmx:afterSettle", function (event) {
  const $grid = $(".entry-list").isotope({
    itemSelector: '.entry-list-item',
    // layoutMode: 'fitRows',
  });

  $('.filter-button-group').on( 'click', 'button', function( event ) {
    // change .active class on buttons
    var $target = $( event.currentTarget );
    $target.toggleClass('active');

    // add or remove filter
    var isChecked = $target.hasClass('active');
    var filter = $target.attr('data-filter');
    if ( isChecked ) {
      addFilter( filter );
    } else {
      removeFilter( filter );
    }
    // apply filters, filters are inclusive (e.g. if two filters, show items that match either)
    $grid.isotope({ filter: filters.join(',') });

  });

});
