# Instruções de Configuração - Sistema de Leilões com gRPC

## 1. Instalar Dependências

```powershell
pip install grpcio grpcio-tools protobuf requests
```

## 2. Gerar Código Python a partir dos arquivos .proto

```powershell
# Criar diretório para código gerado
mkdir generated

# Compilar arquivos proto
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/leilao.proto ./protos/lance.proto ./protos/pagamento.proto ./protos/gateway.proto
```

## 3. Iniciar os Microsserviços

Em terminais separados, execute:

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

## 4. Portas dos Serviços

- **ms_leilao**: localhost:50051
- **ms_lance**: localhost:50052
- **ms_pagamento**: localhost:50053
- **API Gateway**: localhost:50054

## 5. Serviço Externo de Pagamento (Opcional)

```powershell
python services/pagamento.py
```
Porta: localhost:5001

## Observações

- **Removido**: Flask, RabbitMQ, Redis, SSE
- **Adicionado**: gRPC puro para toda comunicação
- **Streaming**: Notificações em tempo real via gRPC Server Streaming
- **Frontend**: Requer gRPC-Web com proxy Envoy (ver documentação abaixo)

## Configuração do Frontend com gRPC-Web

Para conectar o frontend JavaScript aos serviços gRPC, você precisará:

1. Instalar e configurar o Envoy Proxy
2. Ou usar grpcwebproxy
3. Ou implementar um wrapper HTTP simples no Gateway

Consulte a documentação em: https://github.com/grpc/grpc-web
