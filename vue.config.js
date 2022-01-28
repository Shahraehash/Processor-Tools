module.exports = {
  devServer: {
    proxy: 'http://127.0.0.1:5000/'
  },
  transpileDependencies: [
    'vuetify'
  ],
  outputDir: process.env.BASE_URL ? `../static${process.env.BASE_URL}` : "dist",
  // publicPath: process.env.BASE_URL ? '/preprocessor/', : './'

  // relative to outputDir
  assetsDir: "static",
  publicPath: process.env.BASE_URL ? process.env.BASE_URL : './'
}
