const path = require('path');
const webpack = require('webpack');
const ManifestPlugin = require('webpack-manifest-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const mode = process.env.NODE_ENV || 'development';
const hash = {
  'development': '',
  'production': '[hash].',
  'test': '',
};

const banner = `Copyright 2018 Peter Debelak

Sarabande is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sarabande is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sarabande.  If not, see <http://www.gnu.org/licenses/>.`;

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
    path: path.resolve(__dirname, './sarabande/static'),
    publicPath: '/',
    filename: `[name].${hash[mode]}js`,
    chunkFilename: `[name].${hash[mode]}js`,
  },
  devServer: {
    port: process.env.PORT || 5001,
    host: 'localhost',
    contentBase: './sarabande/static',
    publicPath: '/',
		compress: true,
  },
  plugins: [
    new ManifestPlugin({ publicPath: '/static/' }),
    new ExtractTextPlugin({ filename: `[name].${hash[mode]}css` }),
    new webpack.BannerPlugin(banner),
  ],
};
