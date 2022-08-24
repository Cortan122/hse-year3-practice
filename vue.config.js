const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.performance
      .maxEntrypointSize(500000)
      .maxAssetSize(400000)
  }
})
