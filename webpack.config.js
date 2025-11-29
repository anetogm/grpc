const path = require("path");

module.exports = {
  entry: {
    script: "./static/script.js",
    pagamento: "./static/pagamento.js",
  },
  output: {
    path: path.resolve(__dirname, "static/dist"),
    filename: "[name].bundle.js",
  },
  mode: "development",
  devtool: "source-map",
};
