/**
 * Webpack configuration for building standalone JavaScript bundle.
 *
 * This bundle is embedded in exported HTML files and includes:
 * - D3.js (selection, force, zoom, drag modules)
 * - NetVis graph rendering code
 * - Settings and color schemes
 *
 * Output: net_vis/resources/netvis-standalone.min.js
 */

const path = require('path');

module.exports = {
  mode: 'production',
  entry: './src/standalone.ts',
  output: {
    filename: 'netvis-standalone.min.js',
    path: path.resolve(__dirname, 'net_vis/resources'),
    library: {
      name: 'netvis',
      type: 'window',
    },
  },
  resolve: {
    extensions: ['.ts', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  // Inline all D3 modules into the bundle
  externals: {},
};
