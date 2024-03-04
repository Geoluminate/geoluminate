const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const BASE_DIR = path.resolve(__dirname, '../../');


const BundleOutputPath = path.resolve(BASE_DIR, './geoluminate/static/bundles/');
const ContextPath = path.resolve(__dirname, '../');
const ExcludePath = path.resolve(__dirname, '../src/ts/old/');

const VendorDir = path.resolve(__dirname, '../src/vendors/');

console.log('Webpack common config:');
console.log('Output Path:', BundleOutputPath);
console.log('Context Path:', ContextPath);

module.exports = {

  target: 'web',
  context: path.join(__dirname, '../'),
  entry: {
    jquery: 'jquery',
    bootstrap: path.resolve(VendorDir, './bootstrap'),
    // datatables: path.resolve(VendorDir, './datatables'),
    htmx: 'htmx.org',
    justGage: path.resolve(VendorDir, './justGage'),
    list: path.resolve(__dirname, '../src/list'),
    detail: path.resolve(__dirname, '../src/detail'),
    project: path.resolve(__dirname, '../src/project'),
  },
  output: {
    path: BundleOutputPath,
    publicPath: '/static/bundles/',
    filename: 'js/[name]-[fullhash].js',
    chunkFilename: 'js/[name]-[hash].js',
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(BASE_DIR, './geoluminate/conf/'),
      filename: 'webpack-stats.json',
    }),
    new MiniCssExtractPlugin({
      filename: 'css/[name].[contenthash].css'
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
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  externals: {
    project: {
      bootstrap: 'bootstrap'
    },
    list: {
      bootstrap: 'bootstrap'
    },
    detail: {
      bootstrap: 'bootstrap'
    },
    "jquery": "jQuery",
  },
  // optimization: {
  //   splitChunks: {
  //     chunks: 'all',
  //     maxSize: 244000,
  //   },
  // },
};
