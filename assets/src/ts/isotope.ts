// import $ from 'jquery'
import Isotope from 'isotope-layout'

document.addEventListener("htmx:afterSettle", function (event) {
  var el = document.querySelector('.entry-list')

  if (el) {
    const iso = new Isotope('.entry-list', {
      itemSelector: '.entry-list-item',
      layoutMode: 'fitRows',

    })
  }

  //   // filter items on button click
  //   $('.filter-button-group').on('click', 'button', function () {
  //     const filterValue = $(this).attr('data-filter')
  //     $grid.isotope({ filter: filterValue })
  //   })


})

