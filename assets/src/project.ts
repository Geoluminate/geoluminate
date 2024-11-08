import 'htmx.org'
import './alpine'
import './bootstrap'

declare global {
  interface Window {
    htmx: any;
  }
}

window.htmx = require('htmx.org')
