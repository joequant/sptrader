module.exports = {
    entry: "./static/sptrader.js",
    output: {
	filename: "static/bundle.js"
    },
    module: {
	loaders: [
	    { test: /\.js$/,
	      loader: 'babel-loader',
	      exclude: /node_modules/,
	      include: __dirname,
	      options: {
		  retainLines: true,
		  cacheDirectory: true,
		  plugins: ['transform-runtime'],
		  presets: ['es2015', 'react', 'stage-0']
	      }
	    }
	]
    }
}
process.traceDeprecation = true

