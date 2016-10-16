module.exports = {
    entry: "./static/sptrader.js",
    output: {
	filename: "static/bundle.js"
    },
    devtool: "cheap-module-source-map",
    module: {
	loaders: [
	    { test: /\.js$/,
	      loader: 'babel-loader',
	      exclude: /node_modules/,
	      include: __dirname,
	      query: {
		  retainLines: true,
		  cacheDirectory: true,
		  plugins: ['transform-runtime'],
		  presets: ['es2015', 'react', 'stage-2']
	      }
	    }
	]
    }
}
