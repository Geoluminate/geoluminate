import '@popperjs/core'
import {
  Popover,
  Toast,
  Tooltip
} from 'bootstrap'

// initialise bootstrap components
Array.from(document.querySelectorAll('.toast')).forEach(toastNode => new Toast(toastNode))

Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]')).forEach(tooltipNode => new Tooltip(tooltipNode))

Array.from(document.querySelectorAll('[data-bs-toggle="popover"]')).forEach(popoverNode => new Popover(popoverNode, {
  trigger: 'hover'
}))
