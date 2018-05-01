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
    admin: './assets/admin.js',
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
        test: /\.s?css$/,
        use: ExtractTextPlugin.extract({
          use: ['css-loader', 'sass-loader'],
          fallback: 'style-loader',
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
    publicPath: '/',
		compress: true,
  },
  plugins: [
    new ManifestPlugin({ publicPath: '/static/' }),
    new ExtractTextPlugin({ filename: `[name].${hash[mode]}css` }),
  ],
};
