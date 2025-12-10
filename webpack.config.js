const path = require("path");

module.exports = {
  entry: "./static/grpc_entry.js", // Arquivo de entrada que importa tudo
  output: {
    filename: "grpc_client.bundle.js",
    path: path.resolve(__dirname, "static"),
  },
  mode: "production",
};
