"use strict";
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const path = require('path');
const webpack = require('webpack');

const BUILD_DIR = path.resolve(__dirname, '../../frontend/static');
const APP_DIR = path.resolve(__dirname, '../../frontend/js');

const extractSass = new ExtractTextPlugin({
  filename: "[name].[contenthash].css",
  disable: process.env.NODE_ENV === "development"
});

const config = {
  context: __dirname,

  entry: [
    APP_DIR + '/entry.jsx',
  ],

  output: {
    path: BUILD_DIR,
    filename: '[name]-[hash].js'
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        include: APP_DIR,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        },
      },
      { // scss loader for webpack
        test: /\.scss$/,
        use: extractSass.extract({
          use: [{
            loader: "css-loader"
          }, {
            loader: "sass-loader"
          }],
          // use style-loader in development
          fallback: "style-loader"
        })
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: "css-loader"
        })
      },
      {
        test: /\.styl$/,
        loader: 'style!css!stylus'
      },
      {
        test: /\.(mp4|webm|mp3|ogg|wav|jpeg|jpg|bmp|ico|png|gif|ttf|otf|woff|eot)$/,
        loader: 'file?name=[path][name].[ext]?[hash]'
      }
    ]
  },

  plugins: [
    new webpack.NoEmitOnErrorsPlugin(),
    new BundleTracker({filename: './webpack-stats.json'}),
    extractSass,
  ],
};

module.exports = config;
