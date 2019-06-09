const BundleTracker = require("webpack-bundle-tracker")
const webpack = require("webpack")

let production = process.env.NODE_ENV === "production"
var baseUrl = production ? "schichtplaner" : ""

module.exports = {
    baseUrl: production ? `/${baseUrl}/static` : "http://0.0.0.0:8081/",
    outputDir: "./dist/",

    chainWebpack: config => {
        config.optimization.splitChunks(false)

        config
            .plugin("base-url")
            .use(new webpack.DefinePlugin({ __BASE_URL__: `"${baseUrl}"` }))

        config
            .plugin("BundleTracker")
            .use(BundleTracker, [
                { filename: "../frontend/webpack-stats.json" }
            ])

        config.resolve.alias.set("__STATIC__", "static")

        config.devServer
            .public("http://0.0.0.0:8081")
            .host("0.0.0.0")
            .port(8081)
            .hotOnly(true)
            .watchOptions({ poll: 1000 })
            .https(false)
            .headers({ "Access-Control-Allow-Origin": ["*"] })
    }
}
