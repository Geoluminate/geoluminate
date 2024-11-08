import Alpine from 'alpinejs'

Alpine.data('theme', () => ({
  theme: Alpine.$persist('auto'), // Persisted theme state
  systemTheme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',

  get activeTheme() {
    return this.theme === 'auto' ? this.systemTheme : this.theme
  },

  init() {
    // Watch for system theme changes and update dynamically
    this.updateSystemTheme()
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      this.updateSystemTheme()
    })
  },

  updateSystemTheme() {
    this.systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  },

  cycleTheme() {
    this.theme = this.theme === 'light' ? 'dark' : this.theme === 'dark' ? 'auto' : 'light'
  }
}))