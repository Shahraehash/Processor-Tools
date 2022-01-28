module.exports = {
  devServer: {
    proxy: 'http://127.0.0.1:5000/'
  },
  transpileDependencies: [
    'vuetify'
  ],
  outputDir: process.env.BASE_URL ? `../static${process.env.BASE_URL}` : "dist",

  // relative to outputDir
  assetsDir: "static",
  publicPath: './'
}
