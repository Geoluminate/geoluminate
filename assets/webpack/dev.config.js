const { merge } = require('webpack-merge')
const commonConfig = require('./common.config')

module.exports = merge(commonConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  watchOptions: {
    poll: true,
    ignored: /node_modules/
  },
  devServer: {
    port: 3000,
    proxy: {
      '/': 'http://localhost:8000',
    },

    client: {
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: true,
      },
    },
    // We need hot=false (Disable HMR) to set liveReload=true
    hot: false,
    liveReload: true,
  },
})
