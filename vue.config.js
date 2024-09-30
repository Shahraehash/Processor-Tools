module.exports = {
  devServer: {
    proxy: 'http://backend:5000'
    // this is configured to proxy for the docker-compose-dev.yml file
    // if you are running outside of docker, you'll need to change this
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
