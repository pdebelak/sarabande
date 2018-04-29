const path = require('path');
const ManifestPlugin = require('webpack-manifest-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const mode = process.env.NODE_ENV || 'development';
const hash = {
  'development': '',
  'production': '[hash].',
  'test': '',
};

module.exports = {
  entry: {
    app: './assets/index.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          use: ['css-loader', 'sass-loader'],
        })
      },
    ],
  },
  mode: mode,
  resolve: {
    extensions: ['.js', '.css']
  },
  output: {
    path: path.resolve(__dirname, './simple_site/static'),
    publicPath: '/',
    filename: `[name].${hash[mode]}js`,
    chunkFilename: `[name].${hash[mode]}js`,
  },
  devServer: {
    port: process.env.PORT || 5001,
    host: 'localhost',
    contentBase: './simple_site/static',
    publicPath: '/static',
		compress: true,
  },
  plugins: [
    new ManifestPlugin(),
    new ExtractTextPlugin({ filename: `[name].${hash[mode]}css` }),
  ],
};
