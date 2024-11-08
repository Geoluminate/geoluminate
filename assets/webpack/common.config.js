const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const { popper } = require('@popperjs/core')

const BaseDir = path.resolve(__dirname, '../../')
const BundleDir = path.resolve(BaseDir, './geoluminate/static/bundles/')
const AssetsDir = path.resolve(__dirname, '../')
const VendorDir = path.resolve(__dirname, '../src/vendors/')

module.exports = {
  target: 'web',
  context: path.join(__dirname, '../'),
  entry: {
    popper: "@popperjs/core",
    project: path.resolve(__dirname, '../src/project'),
  },
  output: {
    path: BundleDir,
    publicPath: '/static/js/',
    filename: 'js/[name].js',
    // filename: 'js/[name].js',
    // chunkFilename: 'js/[name].js',
  },
  plugins: [
    new BundleTracker({
      relativePath: true,
      path: AssetsDir,
      filename: 'webpack-stats.json',
    }),
    new MiniCssExtractPlugin({
      filename: 'css/[name].[contenthash].css'
      // filename: 'css/[name].css'
    }),

  ],
  module: {
    rules: [
      // we pass the output from babel loader to react-hot loader
      {
        test: /\.js$/,
        loader: 'babel-loader',
      },
      {
        test: /\.tsx?$/,
        exclude: path.resolve(
          __dirname,
          '../node_modules/',
        ),
        use: 'ts-loader',
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['postcss-preset-env', 'autoprefixer', 'pixrem'],
              },
            },
          },
          'sass-loader',
        ],
      },
    ],
  },
  resolve: {
    modules: ['node_modules'],
    extensions: ['.ts', '.tsx', '.js', '.jsx', '.mjs'],
  },
  // optimization: {
  //   splitChunks: {
  //     chunks: 'all',
  //     maxSize: 244000,
  //   },
  // },
}
