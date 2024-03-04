function addFilterListeners() {
  const clearButtons = document.querySelectorAll('.list-filter-clear')

  // Iterate over each button and add an event listener
  clearButtons.forEach(button => {
    button.addEventListener('htmx:before-request', function (event) {
      const el = document.querySelectorAll('.list-filter-form')[0] as HTMLFormElement
      el.reset()
    })
  })
}

// Add the event listener when the DOM is ready
addFilterListeners()

// Add the event listener when an htmx request is complete
document.body.addEventListener('htmx:after-settle', addFilterListeners)
