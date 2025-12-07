# Tutorial: Configuração do gRPC Web para Frontend

Este tutorial explica como configurar o gRPC Web para o frontend do projeto, permitindo que o navegador se comunique com os serviços gRPC.

## Passos

### 1. Criar package.json

Crie um arquivo `package.json` na raiz do projeto com as seguintes dependências:

```json
{
  "name": "grpc-frontend",
  "version": "1.0.0",
  "description": "Frontend gRPC Web client",
  "scripts": {
    "build": "webpack --mode=production"
  },
  "dependencies": {
    "grpc-web": "^1.4.2"
  },
  "devDependencies": {
    "webpack": "^5.89.0",
    "webpack-cli": "^5.1.4"
  }
}
```

### 2. Instalar dependências

Execute no terminal:

```bash
npm install
```

### 3. Instalar plugin protoc-gen-grpc-web

Execute:

```bash
npm install protoc-gen-grpc-web --save-dev
```

### 4. Gerar código JavaScript dos arquivos .proto

Execute:

```bash
protoc --js_out=import_style=commonjs:static --grpc-web_out=import_style=commonjs,mode=grpcwebtext:static --proto_path=protos protos/*.proto
```

Isso gera arquivos `*_pb.js` e `*_grpc_web_pb.js` na pasta `static`.

### 5. Criar webpack.config.js

Crie um arquivo `webpack.config.js` na raiz:

```javascript
const path = require("path");

module.exports = {
  entry: "./static/app.js",
  output: {
    filename: "grpc_client.bundle.js",
    path: path.resolve(__dirname, "static"),
  },
  mode: "production",
};
```

### 6. Executar build

Execute:

```bash
npm run build
```

Isso gera o `grpc_client.bundle.js` atualizado na pasta `static`.

## Observações

- Para o gRPC Web funcionar no navegador, é necessário um proxy (como Envoy) para traduzir HTTP/1.1 em gRPC.
- Verifique se o Gateway (porta 50054) está configurado como proxy gRPC Web.
