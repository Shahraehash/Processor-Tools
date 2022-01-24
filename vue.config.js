module.exports = {
  devServer: {
    proxy: 'http://127.0.0.1:5000/'
  },
  transpileDependencies: [
    'vuetify'
  ],
  outputDir: "../static/preprocessor",

  // relative to outputDir
  assetsDir: "static",
  publicPath: './'
}
