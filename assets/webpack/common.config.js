const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const BaseDir = path.resolve(__dirname, '../../');
const BundleDir = path.resolve(BaseDir, './geoluminate/static/bundles/');
const AssetsDir = path.resolve(__dirname, '../');
const VendorDir = path.resolve(__dirname, '../src/vendors/');

console.log('Webpack common config:');
console.log('Output Path:', BundleDir);
console.log('Context Path:', AssetsDir);

module.exports = {
  target: 'web',
  context: path.join(__dirname, '../'),
  entry: {
    jquery: 'jquery',
    bootstrap: path.resolve(VendorDir, './bootstrap'),
    datatables: path.resolve(AssetsDir, './src/datatables/index'),
    htmx: 'htmx.org',
    justGage: path.resolve(VendorDir, './justGage'),
    list: path.resolve(__dirname, '../src/list'),
    detail: path.resolve(__dirname, '../src/detail'),
    project: path.resolve(__dirname, '../src/project'),
  },
  output: {
    path: BundleDir,
    publicPath: '/static/bundles/',
    filename: 'js/[name]-[fullhash].js',
    // filename: 'js/[name].js',
    chunkFilename: 'js/[name]-[hash].js',
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
  externals: {
    project: {
      bootstrap: 'bootstrap'
    },
    list: {
      bootstrap: 'bootstrap'
    },
    detail: {
      bootstrap: 'bootstrap',
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
