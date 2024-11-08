const {
  merge
} = require('webpack-merge')
const commonConfig = require('./common.config')
const BundleTracker = require('webpack-bundle-tracker')
const path = require('path')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const BaseDir = path.resolve(__dirname, '../../')

// This variable should mirror the one from config/settings/production.py
const staticUrl = '/static/'
const BASE_DIR = path.resolve(__dirname, '../../')


module.exports = merge(commonConfig, {
  mode: 'production',
  devtool: false,
  bail: true,
  output: {
    publicPath: `${staticUrl}bundles/`,
  },
  plugins: [
    new BundleTracker({
      relativePath: true,
      path: path.resolve(BASE_DIR, './geoluminate/conf/'),
      filename: 'webpack-stats.prod.json',
    }),
    new CopyWebpackPlugin({
      patterns: [{
        from: path.resolve(BaseDir, 'node_modules/bootstrap/scss/'),
        to: path.resolve(BaseDir, 'geoluminate/static/bs5/'),
      },],
    }),
  ],
})
