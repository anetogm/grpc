# Sistema de Leilões com gRPC

Sistema de leilões distribuído implementado com **gRPC puro**, removendo completamente RabbitMQ, REST e SSE.

## 📋 Arquitetura

```
┌─────────────┐
│   Frontend  │ (gRPC-Web ou cliente gRPC)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Gateway    │ :50054 (API Gateway gRPC)
└──────┬──────┘
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ ms_leilao│   │ ms_lance │   │ms_pagamen│   │ pagamento│
│  :50051  │   │  :50052  │   │   :50053 │   │  :5001   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

## 🚀 Início Rápido

### 1. Instalar Dependências

```powershell
pip install grpcio grpcio-tools protobuf requests
```

### 2. Gerar Código a partir dos .proto

```powershell
mkdir generated
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/leilao.proto ./protos/lance.proto ./protos/pagamento.proto ./protos/gateway.proto
```

### 3. Iniciar os Microsserviços

Abra **4 terminais** separados e execute:

```powershell
# Terminal 1 - Microsserviço de Leilão
python services/ms_leilao.py

# Terminal 2 - Microsserviço de Lance  
python services/ms_lance.py

# Terminal 3 - Microsserviço de Pagamento
python services/ms_pagamento.py

# Terminal 4 - API Gateway
python app.py
```

### 4. (Opcional) Serviço Externo de Pagamento

```powershell
python services/pagamento.py
```

## 📡 Portas dos Serviços

| Serviço | Porta | Protocolo |
|---------|-------|-----------|
| ms_leilao | 50051 | gRPC |
| ms_lance | 50052 | gRPC |
| ms_pagamento | 50053 | gRPC |
| API Gateway | 50054 | gRPC |
| Serv. Externo | 5001 | HTTP (REST) |

## 📝 Definições dos Serviços

### LeilaoService (porta 50051)
- `CriarLeilao` - Criar novo leilão
- `ListarLeiloes` - Listar leilões ativos
- `RegistrarInteresse` - Cliente registra interesse
- `CancelarInteresse` - Cliente cancela interesse
- `StreamNotificacoes` - Stream de notificações do leilão (Server Streaming)

### LanceService (porta 50052)
- `EnviarLance` - Enviar lance para leilão
- `IniciarLeilao` - Notificar início de leilão (chamado por ms_leilao)
- `FinalizarLeilao` - Notificar fim de leilão (chamado por ms_leilao)
- `StreamLances` - Stream de notificações de lances (Server Streaming)

### PagamentoService (porta 50053)
- `ProcessarPagamento` - Processar pagamento
- `NotificarVencedor` - Notificar vencedor (chamado por ms_lance)
- `StreamPagamentos` - Stream de notificações de pagamento (Server Streaming)

### GatewayService (porta 50054)
- Agrega todos os métodos dos serviços acima
- `StreamNotificacoesUnificadas` - Stream unificado de todas as notificações (Server Streaming)

## 🔄 Fluxo de Comunicação

### 1. Criar Leilão
```
Frontend → Gateway.CriarLeilao → LeilaoService.CriarLeilao
```

### 2. Registrar Interesse
```
Frontend → Gateway.RegistrarInteresse → LeilaoService.RegistrarInteresse
```

### 3. Conectar ao Stream
```
Frontend → Gateway.StreamNotificacoesUnificadas →
  → LeilaoService.StreamNotificacoes
  → LanceService.StreamLances  
  → PagamentoService.StreamPagamentos
```

### 4. Início do Leilão
```
ms_leilao (timer) → LanceService.IniciarLeilao
ms_leilao → LeilaoService.StreamNotificacoes → Gateway → Frontend
```

### 5. Enviar Lance
```
Frontend → Gateway.EnviarLance → LanceService.EnviarLance
LanceService valida lance → LanceService.StreamLances → Gateway → Frontend
```

### 6. Finalizar Leilão
```
ms_leilao (timer) → LanceService.FinalizarLeilao
LanceService → PagamentoService.NotificarVencedor
PagamentoService → Serviço Externo (HTTP)
PagamentoService.StreamPagamentos → Gateway → Frontend
```

## 🌐 Frontend com gRPC-Web

Para conectar um frontend web JavaScript aos serviços gRPC, você tem 3 opções:

### Opção 1: Envoy Proxy (Recomendado)
```yaml
# envoy.yaml
static_resources:
  listeners:
    - address:
        socket_address:
          address: 0.0.0.0
          port_value: 8080
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                codec_type: AUTO
                stat_prefix: ingress_http
                route_config:
                  name: local_route
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match: { prefix: "/" }
                          route: { cluster: gateway_service }
                      cors:
                        allow_origin_string_match:
                          - prefix: "*"
                        allow_methods: "GET, POST, PUT, DELETE, OPTIONS"
                        allow_headers: "content-type,x-grpc-web,x-user-agent"
                        expose_headers: "grpc-status,grpc-message"
                http_filters:
                  - name: envoy.filters.http.grpc_web
                  - name: envoy.filters.http.cors
                  - name: envoy.filters.http.router

  clusters:
    - name: gateway_service
      connect_timeout: 0.25s
      type: LOGICAL_DNS
      http2_protocol_options: {}
      lb_policy: ROUND_ROBIN
      load_assignment:
        cluster_name: gateway_service
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: localhost
                      port_value: 50054
```

Executar:
```powershell
docker run -d -p 8080:8080 -v ${PWD}/envoy.yaml:/etc/envoy/envoy.yaml envoyproxy/envoy:v1.28-latest
```

### Opção 2: grpcwebproxy
```powershell
grpcwebproxy --backend_addr=localhost:50054 --run_tls_server=false --allow_all_origins
```

### Opção 3: Cliente gRPC Python (para testes)
```python
import grpc
import gateway_pb2
import gateway_pb2_grpc

# Conectar ao Gateway
channel = grpc.insecure_channel('localhost:50054')
stub = gateway_pb2_grpc.GatewayServiceStub(channel)

# Listar leilões
response = stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
for leilao in response.leiloes:
    print(f"Leilão {leilao.id}: {leilao.nome}")

# Stream de notificações
for notificacao in stub.StreamNotificacoesUnificadas(
    gateway_pb2.StreamNotificacoesUnificadasRequest(cliente_id="user123")
):
    print(f"Notificação: {notificacao.tipo}")
```

## 🔧 Testando com grpcurl

```powershell
# Instalar grpcurl
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# Listar serviços
grpcurl -plaintext localhost:50054 list

# Chamar método
grpcurl -plaintext -d '{}' localhost:50054 gateway.GatewayService/ListarLeiloes

# Stream de notificações
grpcurl -plaintext -d '{"cliente_id": "user123"}' localhost:50054 gateway.GatewayService/StreamNotificacoesUnificadas
```

## ✅ Mudanças Implementadas

### ❌ Removido
- ✅ Flask e todas as rotas REST
- ✅ RabbitMQ e toda comunicação pub/sub
- ✅ Redis para gerenciar interesses
- ✅ SSE (Server-Sent Events)
- ✅ Dependências: `flask`, `flask-cors`, `flask-sse`, `pika`, `redis`

### ✅ Adicionado
- ✅ Arquivos `.proto` para definir contratos gRPC
- ✅ Servidores gRPC em todos os microsserviços
- ✅ API Gateway gRPC que agrega todos os serviços
- ✅ gRPC Server Streaming para notificações em tempo real
- ✅ Comunicação direta entre microsserviços via gRPC
- ✅ Dependências: `grpcio`, `grpcio-tools`, `protobuf`

## 📚 Referências

- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [gRPC-Web](https://github.com/grpc/grpc-web)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
- [Envoy Proxy](https://www.envoyproxy.io/)

## 🐛 Troubleshooting

### Erro: "No module named 'gateway_pb2'"
Execute a geração dos arquivos proto:
```powershell
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/*.proto
```

### Erro: "failed to connect to all addresses"
Verifique se os microsserviços estão rodando nas portas corretas.

### Frontend não conecta
Configure o Envoy Proxy ou grpcwebproxy para fazer a ponte entre HTTP/1.1 e HTTP/2.

## 📄 Licença

Este projeto é um exemplo educacional para demonstrar arquitetura de microsserviços com gRPC.
