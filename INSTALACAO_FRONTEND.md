# 🚀 Instalação do Frontend gRPC-Web

Este guia detalha o processo completo para migrar o frontend para gRPC-Web usando Envoy Proxy.

## 📋 Pré-requisitos

### 1. Docker Desktop

- Baixe: https://www.docker.com/products/docker-desktop
- Instale e inicie o Docker Desktop

### 2. Node.js e npm

- Baixe: https://nodejs.org/ (versão LTS)
- Verifique a instalação:

```powershell
node --version
npm --version
```

### 3. Protocol Buffers Compiler (protoc)

- Baixe: https://github.com/protocolbuffers/protobuf/releases
- Escolha `protoc-XX.X-win64.zip`
- Extraia e adicione ao PATH

### 4. Plugin gRPC-Web para protoc

- Baixe: https://github.com/grpc/grpc-web/releases
- Escolha `protoc-gen-grpc-web-X.X.X-windows-x86_64.exe`
- Renomeie para `protoc-gen-grpc-web.exe`
- Coloque no mesmo diretório do protoc ou adicione ao PATH

## 🔧 Passo a Passo

### 1. Instalar Dependências Node.js

```powershell
npm install
```

Isso instalará:

- `grpc-web`: Cliente gRPC-Web
- `google-protobuf`: Biblioteca Protocol Buffers
- `webpack`: Bundler para JavaScript

### 2. Gerar Código JavaScript

```powershell
.\generate_grpc_web.ps1
```

Ou manualmente:

```powershell
protoc -I=.\protos `
  --js_out=import_style=commonjs:.\static\generated `
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:.\static\generated `
  .\protos\leilao.proto `
  .\protos\lance.proto `
  .\protos\pagamento.proto `
  .\protos\gateway.proto
```

**Arquivos gerados em `static/generated/`:**

- `leilao_pb.js` - Mensagens
- `leilao_grpc_web_pb.js` - Cliente do serviço
- `lance_pb.js`
- `lance_grpc_web_pb.js`
- `pagamento_pb.js`
- `pagamento_grpc_web_pb.js`
- `gateway_pb.js`
- `gateway_grpc_web_pb.js`

### 3. Iniciar Envoy Proxy

```powershell
docker-compose up -d
```

**Verificar logs:**

```powershell
docker-compose logs -f envoy
```

**Verificar status:**

- Admin: http://localhost:9901
- Proxy: http://localhost:8080

### 4. Iniciar Backend gRPC

Em **4 terminais separados**, ative o venv e execute:

**Terminal 1:**

```powershell
.\venv\Scripts\Activate.ps1
python services\ms_leilao.py
```

**Terminal 2:**

```powershell
.\venv\Scripts\Activate.ps1
python services\ms_lance.py
```

**Terminal 3:**

```powershell
.\venv\Scripts\Activate.ps1
python services\ms_pagamento.py
```

**Terminal 4:**

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

### 5. Servir Frontend

Opção 1 - Python HTTP Server:

```powershell
python -m http.server 3000
```

Opção 2 - Node.js http-server:

```powershell
npm install -g http-server
http-server -p 3000
```

### 6. Acessar Aplicação

Abra no navegador:

```
http://localhost:3000/templates/index.html
```

## 🧪 Testar a Conexão

Abra o Console do Navegador (F12) e execute:

```javascript
// Importar módulos (se usando webpack)
const {
  GatewayServiceClient,
} = require("./static/generated/gateway_grpc_web_pb");
const { ListarLeiloesRequest } = require("./static/generated/leilao_pb");

// Criar cliente
const client = new GatewayServiceClient("http://localhost:8080");

// Listar leilões
const request = new ListarLeiloesRequest();
client.listarLeiloes(request, {}, (err, response) => {
  if (err) {
    console.error("Erro:", err);
  } else {
    console.log("Leilões:", response.getLeiloesList());
  }
});
```

## 🔄 Fluxo de Dados Completo

```
┌─────────────┐
│  Navegador  │
│ localhost:  │
│    3000     │
└──────┬──────┘
       │ HTTP/1.1 (gRPC-Web)
       │
┌──────▼──────┐
│   Envoy     │
│ localhost:  │
│    8080     │
└──────┬──────┘
       │ HTTP/2 (gRPC puro)
       │
┌──────▼──────┐
│ API Gateway │
│ localhost:  │
│   50054     │
└──────┬──────┘
       │
   ┌───┴───────────────┐
   │                   │
┌──▼────┐  ┌──────┐  ┌▼────────┐
│ms_    │  │ms_   │  │ms_      │
│leilao │  │lance │  │pagamento│
│:50051 │  │:50052│  │:50053   │
└───────┘  └──────┘  └─────────┘
```

## 🛠️ Comandos Úteis

### Docker

```powershell
# Iniciar Envoy
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar Envoy
docker-compose down

# Rebuild
docker-compose up --build -d

# Ver containers rodando
docker ps
```

### Verificar Portas

```powershell
# Windows
netstat -ano | findstr "8080"
netstat -ano | findstr "50054"
netstat -ano | findstr "3000"
```

## ❓ Troubleshooting

### Erro: "protoc not found"

- Certifique-se que protoc está no PATH
- Verifique: `protoc --version`

### Erro: "protoc-gen-grpc-web not found"

- Baixe o plugin do GitHub releases
- Renomeie para `protoc-gen-grpc-web.exe`
- Coloque no PATH

### Erro: "Cannot connect to localhost:8080"

- Verifique se Envoy está rodando: `docker ps`
- Veja logs: `docker-compose logs envoy`
- Teste admin: http://localhost:9901

### Erro: "Cannot connect to localhost:50054"

- Verifique se API Gateway está rodando
- Teste com: `python test_grpc.py`

### Erro: CORS no navegador

- Verifique configuração CORS no `envoy.yaml`
- Certifique-se de usar `http://localhost:8080` (não IP)

### Erro: Stream não funciona

- gRPC-Web streams são unários (client → server) ou server streaming
- Não suporta bi-direcional como gRPC puro

## 📚 Próximos Passos

Após concluir a instalação:

1. Migre `script.js` → `script_grpc.js`
2. Migre `pagamento.js` → `pagamento_grpc.js`
3. Atualize `index.html` para usar bundles webpack
4. Teste todas as funcionalidades

---

**Versão**: 1.0  
**Data**: 29/11/2025  
**Status**: Pronto para instalação
