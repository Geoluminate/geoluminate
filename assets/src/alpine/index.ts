import Alpine from 'alpinejs'
import mask from '@alpinejs/mask'
import persist from '@alpinejs/persist'
import morph from '@alpinejs/morph'

import "./theme"

declare global {
  interface Window {
    Alpine: typeof Alpine
  }
}

window.Alpine = Alpine

Alpine.plugin(mask)
Alpine.plugin(persist)
Alpine.plugin(morph)

Alpine.start()
