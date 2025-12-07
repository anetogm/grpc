const path = require("path");

module.exports = {
  entry: "./static/app.js", // ou o arquivo principal
  output: {
    filename: "grpc_client.bundle.js",
    path: path.resolve(__dirname, "static"),
  },
  mode: "production",
};
