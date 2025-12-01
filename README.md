# 🎯 Sistema de Leilões Distribuído com gRPC

Sistema completo de leilões em tempo real implementado com **arquitetura de microsserviços** usando **gRPC** para comunicação entre serviços e interface web com **Flask** + **JavaScript**.

## 📖 Sobre o Projeto

Este é um sistema de leilões online que demonstra os conceitos fundamentais de **sistemas distribuídos**:
- **Comunicação entre microsserviços** usando gRPC (alta performance)
- **Streaming bidirecional** para notificações em tempo real
- **Desacoplamento** de serviços especializados
- **Escalabilidade horizontal** através de microsserviços independentes
- **Protocol Buffers** para serialização eficiente de dados

## 📋 Arquitetura

```
┌─────────────┐
│   Browser   │ (Frontend HTML + JavaScript)
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│ Web Server  │ :3000 (Flask REST API)
└──────┬──────┘
       │ gRPC
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

## 🚀 Como Usar

### 1. Instalar Dependências

```powershell
pip install grpcio grpcio-tools protobuf requests flask flask-cors
```

### 2. Gerar Código Python dos .proto

```powershell
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/leilao.proto ./protos/lance.proto ./protos/pagamento.proto ./protos/gateway.proto
```

### 3. Iniciar os Microsserviços (5 terminais)

```powershell
# Terminal 1 - Microsserviço de Leilão
python services/ms_leilao.py

# Terminal 2 - Microsserviço de Lance
python services/ms_lance.py

# Terminal 3 - Microsserviço de Pagamento
python services/ms_pagamento.py

# Terminal 4 - Gateway gRPC
python app.py

# Terminal 5 - Servidor Web Flask
python web_server.py
```

### 4. Acessar o Frontend

Abra o navegador em: **http://localhost:3000**

## 📡 Funcionalidades

- ✅ Criar leilões
- ✅ Listar leilões ativos
- ✅ Registrar interesse em leilão
- ✅ Fazer lances
- ✅ Processar pagamentos

## 📡 Portas dos Serviços

| Serviço       | Porta | Protocolo   |
| ------------- | ----- | ----------- |
| Web Server    | 3000  | HTTP        |
| API Gateway   | 50054 | gRPC        |
| ms_leilao     | 50051 | gRPC        |
| ms_lance      | 50052 | gRPC        |
| ms_pagamento  | 50053 | gRPC        |
| Serv. Externo | 5001  | HTTP (REST) |

## 📝 Estrutura do Projeto

```
grpc/
├── protos/           # Definições Protocol Buffers
│   ├── gateway.proto
│   ├── leilao.proto
│   ├── lance.proto
│   └── pagamento.proto
├── generated/        # Código Python gerado
├── services/         # Microsserviços gRPC
│   ├── ms_leilao.py
│   ├── ms_lance.py
│   ├── ms_pagamento.py
│   └── pagamento.py
├── templates/        # Páginas HTML
│   ├── index.html
│   ├── cadastra_leilao.html
│   └── lance.html
├── static/           # JavaScript frontend
│   ├── app.js
│   ├── cadastra.js
│   └── lance.js
├── app.py           # Gateway gRPC
├── web_server.py    # Servidor web Flask
└── README.md
```

## 🔧 Tecnologias

- **Python 3.8+**
- **gRPC** - Comunicação entre microsserviços
- **Protocol Buffers** - Serialização de dados
- **Flask** - Servidor web e API REST
- **JavaScript (Vanilla)** - Frontend

## ⚡ Comandos Rápidos

### Instalar tudo de uma vez:
```powershell
pip install grpcio grpcio-tools protobuf requests flask flask-cors
```

### Gerar código dos .proto:
```powershell
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/leilao.proto ./protos/lance.proto ./protos/pagamento.proto ./protos/gateway.proto
```

### Iniciar todos os serviços (cole em terminais separados):
```powershell
python services/ms_leilao.py
python services/ms_lance.py
python services/ms_pagamento.py
python app.py
python web_server.py
```

Depois acesse: **http://localhost:3000**

---

## 🏗️ Arquitetura Detalhada

### Microsserviços

#### 1️⃣ **ms_leilao** (Porta 50051)
Gerencia o ciclo de vida dos leilões.

**Responsabilidades:**
- Criar novos leilões
- Listar leilões disponíveis
- Gerenciar registro/cancelamento de interesse de clientes
- Notificar início e fim de leilões via timers
- Enviar notificações em tempo real para clientes interessados

**Métodos gRPC:**
```protobuf
service LeilaoService {
  rpc CriarLeilao(CriarLeilaoRequest) returns (CriarLeilaoResponse);
  rpc ListarLeiloes(ListarLeiloesRequest) returns (ListarLeiloesResponse);
  rpc RegistrarInteresse(RegistrarInteresseRequest) returns (RegistrarInteresseResponse);
  rpc CancelarInteresse(CancelarInteresseRequest) returns (CancelarInteresseResponse);
  rpc StreamNotificacoes(StreamNotificacoesRequest) returns (stream NotificacaoLeilao);
}
```

**Estrutura de Dados:**
- Leilões armazenados em lista Python (simulando banco de dados)
- Cada leilão tem: `id`, `nome`, `descricao`, `valor_inicial`, `data_inicio`, `data_fim`, `status`
- Mapa de clientes interessados: `{leilao_id: set(cliente_ids)}`

**Fluxo de Funcionamento:**
1. Cliente chama `CriarLeilao` → Leilão adicionado à lista
2. Thread de timer monitora horários de início/fim
3. No início: chama `LanceService.IniciarLeilao` e notifica clientes via stream
4. No fim: chama `LanceService.FinalizarLeilao` e notifica clientes

---

#### 2️⃣ **ms_lance** (Porta 50052)
Gerencia lances e determina vencedores.

**Responsabilidades:**
- Receber e validar lances
- Determinar lance vencedor ao fim do leilão
- Notificar microsserviço de pagamento sobre vencedores
- Enviar notificações de lances em tempo real

**Métodos gRPC:**
```protobuf
service LanceService {
  rpc EnviarLance(EnviarLanceRequest) returns (EnviarLanceResponse);
  rpc IniciarLeilao(IniciarLeilaoRequest) returns (IniciarLeilaoResponse);
  rpc FinalizarLeilao(FinalizarLeilaoRequest) returns (FinalizarLeilaoResponse);
  rpc StreamLances(StreamLancesRequest) returns (stream NotificacaoLance);
}
```

**Validação de Lances:**
- Verifica se leilão está ativo
- Verifica se valor é maior que lance atual
- Armazena lance e atualiza lance vencedor

**Fluxo ao Finalizar Leilão:**
1. `ms_leilao` chama `FinalizarLeilao`
2. Determina vencedor (maior lance)
3. Chama `PagamentoService.NotificarVencedor`
4. Envia notificação de vencedor para clientes

---

#### 3️⃣ **ms_pagamento** (Porta 50053)
Integra com sistema externo de pagamento.

**Responsabilidades:**
- Processar pagamentos do vencedor
- Comunicar com API externa de pagamento (HTTP)
- Receber webhooks de confirmação/rejeição
- Notificar clientes sobre status do pagamento

**Métodos gRPC:**
```protobuf
service PagamentoService {
  rpc ProcessarPagamento(ProcessarPagamentoRequest) returns (ProcessarPagamentoResponse);
  rpc NotificarVencedor(NotificarVencedorRequest) returns (NotificarVencedorResponse);
  rpc ReceberWebhook(WebhookRequest) returns (WebhookResponse);
  rpc StreamPagamentos(StreamPagamentosRequest) returns (stream NotificacaoPagamento);
}
```

**Integração com Serviço Externo:**
- Faz requisição HTTP POST para `http://localhost:5001/api/pagamento`
- Recebe link de pagamento
- Monitora webhooks do serviço externo
- Notifica cliente via stream quando pagamento é confirmado/rejeitado

---

#### 4️⃣ **Gateway (app.py)** (Porta 50054)
API Gateway que agrega todos os microsserviços.

**Responsabilidades:**
- Ponto único de entrada para clientes
- Roteia requisições para microsserviços corretos
- Agrega streams de notificações de todos os serviços
- Simplifica cliente (apenas 1 conexão gRPC)

**Métodos gRPC:**
```protobuf
service GatewayService {
  // Leilão
  rpc CriarLeilao(CriarLeilaoRequest) returns (CriarLeilaoResponse);
  rpc ListarLeiloes(ListarLeiloesRequest) returns (ListarLeiloesResponse);
  rpc RegistrarInteresse(RegistrarInteresseRequest) returns (RegistrarInteresseResponse);
  rpc CancelarInteresse(CancelarInteresseRequest) returns (CancelarInteresseResponse);
  
  // Lance
  rpc EnviarLance(EnviarLanceRequest) returns (EnviarLanceResponse);
  
  // Pagamento
  rpc ProcessarPagamento(ProcessarPagamentoRequest) returns (ProcessarPagamentoResponse);
  
  // Stream Unificado
  rpc StreamNotificacoesUnificadas(StreamNotificacoesUnificadasRequest) 
      returns (stream NotificacaoUnificada);
}
```

**Stream Unificado:**
- Conecta aos 3 streams dos microsserviços
- Converte notificações para formato unificado
- Envia tudo por 1 único stream para o cliente

---

#### 5️⃣ **Serviço Externo de Pagamento** (Porta 5001)
API REST Flask simulando processador de pagamento externo.

**Endpoints:**
- `POST /api/pagamento` - Iniciar transação
- `GET /pagar/<id_transacao>` - Página de pagamento
- `POST /async?id_transacao=X` - Processar pagamento assíncrono

**Comportamento:**
- Retorna link de pagamento
- Processa pagamento após 3 segundos (simulado)
- Envia webhook para `ms_pagamento` com resultado

---

## 🔄 Fluxos Completos

### 📝 Fluxo: Criar Leilão

```
┌─────────┐      ┌─────────┐      ┌──────────┐
│ Cliente │─────▶│ Gateway │─────▶│ms_leilao │
└─────────┘      └─────────┘      └──────────┘
     │                │                  │
     │  CriarLeilao   │                  │
     │───────────────▶│  CriarLeilao     │
     │                │─────────────────▶│
     │                │                  │ Adiciona leilão
     │                │  Response        │ à lista
     │                │◀─────────────────│
     │  Response      │                  │
     │◀───────────────│                  │
```

### 🔔 Fluxo: Registrar Interesse + Stream

```
┌─────────┐      ┌─────────┐      ┌──────────┐
│ Cliente │      │ Gateway │      │ms_leilao │
└─────────┘      └─────────┘      └──────────┘
     │                │                  │
     │ RegistrarInteresse                │
     │───────────────▶│                  │
     │                │─────────────────▶│ Adiciona cliente
     │                │                  │ à lista de interessados
     │                │                  │
     │ StreamNotificacoesUnificadas      │
     │───────────────▶│                  │
     │                │ StreamNotificacoes
     │                │─────────────────▶│
     │                │                  │
     │◀═══════════════│◀═════════════════│ Stream aberto
     │   (notificações em tempo real)    │
```

### 💰 Fluxo: Enviar Lance

```
┌─────────┐  ┌─────────┐  ┌────────┐  ┌──────────┐
│ Cliente │  │ Gateway │  │ms_lance│  │Clientes  │
│         │  │         │  │        │  │conectados│
└─────────┘  └─────────┘  └────────┘  └──────────┘
     │            │            │             │
     │ EnviarLance│            │             │
     │───────────▶│ EnviarLance│             │
     │            │───────────▶│ Valida lance│
     │            │            │ Atualiza    │
     │            │            │ vencedor    │
     │            │  Response  │             │
     │            │◀───────────│             │
     │  Response  │            │ Notifica    │
     │◀───────────│            │ via stream  │
     │            │            │────────────▶│ NOVO_LANCE
```

### 🏆 Fluxo: Finalizar Leilão e Pagamento

```
┌──────────┐  ┌────────┐  ┌────────────┐  ┌──────────┐  ┌─────────┐
│ms_leilao │  │ms_lance│  │ms_pagamento│  │Serv.Ext. │  │ Cliente │
└──────────┘  └────────┘  └────────────┘  └──────────┘  └─────────┘
     │             │              │              │             │
     │Timer detecta│              │              │             │
     │fim do leilão│              │              │             │
     │             │              │              │             │
     │FinalizarLeilao             │              │             │
     │────────────▶│Determina     │              │             │
     │             │vencedor      │              │             │
     │             │              │              │             │
     │             │NotificarVencedor            │             │
     │             │─────────────▶│              │             │
     │             │              │POST /api/pagamento         │
     │             │              │─────────────▶│             │
     │             │              │              │             │
     │             │              │link_pagamento│             │
     │             │              │◀─────────────│             │
     │             │              │              │             │
     │             │              │Stream────────────────────▶│
     │             │              │  (envia link)│             │
     │             │              │              │             │
     │             │              │              │Cliente acessa
     │             │              │              │link e paga  │
     │             │              │              │             │
     │             │              │◀─Webhook─────│             │
     │             │              │  (aprovado)  │             │
     │             │              │              │             │
     │             │              │Stream────────────────────▶│
     │             │              │  (pagamento OK)            │
```

---

## 📡 Comunicação gRPC

### Tipos de Comunicação Usados

#### 1. **Unary RPC** (Requisição-Resposta simples)
```protobuf
rpc CriarLeilao(CriarLeilaoRequest) returns (CriarLeilaoResponse);
```
Cliente envia 1 requisição → Servidor retorna 1 resposta

#### 2. **Server Streaming RPC** (Servidor envia múltiplas mensagens)
```protobuf
rpc StreamNotificacoes(StreamNotificacoesRequest) returns (stream NotificacaoLeilao);
```
Cliente envia 1 requisição → Servidor retorna stream contínuo de mensagens

**Vantagens:**
- ✅ Baixa latência (conexão persistente)
- ✅ Bidirecional (HTTP/2)
- ✅ Eficiente (Protocol Buffers é binário)
- ✅ Tipo-seguro (contrato definido em .proto)

---

## 📦 Protocol Buffers

### Exemplo: leilao.proto

```protobuf
syntax = "proto3";

message Leilao {
    int32 id = 1;
    string nome = 2;
    string descricao = 3;
    double valor_inicial = 4;
    string inicio = 5;
    string fim = 6;
    string status = 7;  // "ativo", "encerrado"
}

message CriarLeilaoRequest {
    string nome = 1;
    string descricao = 2;
    double valor_inicial = 3;
    string inicio = 4;
    string fim = 5;
}

message CriarLeilaoResponse {
    bool success = 1;
    string message = 2;
    int32 leilao_id = 3;
    Leilao leilao = 4;
}
```

**Gerar código Python:**
```powershell
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/leilao.proto
```

Isso gera:
- `leilao_pb2.py` - Classes de mensagens
- `leilao_pb2_grpc.py` - Stub do cliente e classe base do servidor

## 🔍 Implementação Detalhada

### Servidor gRPC (Exemplo: ms_leilao.py)

```python
import grpc
from concurrent import futures
import leilao_pb2
import leilao_pb2_grpc

class LeilaoServicer(leilao_pb2_grpc.LeilaoServiceServicer):
    def CriarLeilao(self, request, context):
        # Criar leilão
        leilao = {
            'id': len(leiloes) + 1,
            'nome': request.nome,
            'status': 'ativo'
        }
        leiloes.append(leilao)
        
        return leilao_pb2.CriarLeilaoResponse(
            success=True,
            message="Leilão criado!",
            leilao_id=leilao['id']
        )
    
    def StreamNotificacoes(self, request, context):
        # Stream infinito de notificações
        while context.is_active():
            notificacao = fila_notificacoes.get()  # Bloqueia até ter notificação
            yield notificacao

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    leilao_pb2_grpc.add_LeilaoServiceServicer_to_server(
        LeilaoServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

### Cliente gRPC (Exemplo: Gateway chamando ms_leilao)

```python
import grpc
import leilao_pb2
import leilao_pb2_grpc

# Criar canal (conexão persistente)
channel = grpc.insecure_channel('localhost:50051')
stub = leilao_pb2_grpc.LeilaoServiceStub(channel)

# Chamar método
request = leilao_pb2.CriarLeilaoRequest(
    nome="Notebook",
    descricao="Macbook Pro",
    valor_inicial=1000.0,
    inicio="2025-12-01T10:00:00",
    fim="2025-12-01T12:00:00"
)
response = stub.CriarLeilao(request)
print(f"Leilão criado: {response.leilao_id}")

# Receber stream
for notificacao in stub.StreamNotificacoes(
    leilao_pb2.StreamNotificacoesRequest(cliente_id="user123")
):
    print(f"Notificação: {notificacao.tipo}")
```

---

## 🌐 Interface Web (Flask + JavaScript)

### Backend: web_server.py

```python
from flask import Flask, jsonify, request
import grpc
import gateway_pb2_grpc

app = Flask(__name__)
gateway_stub = gateway_pb2_grpc.GatewayServiceStub(
    grpc.insecure_channel('localhost:50054')
)

@app.route('/api/leiloes', methods=['GET'])
def listar_leiloes():
    response = gateway_stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
    leiloes = [
        {
            'id': l.id,
            'nome': l.nome,
            'status': l.status
        }
        for l in response.leiloes
    ]
    return jsonify({'success': True, 'leiloes': leiloes})

@app.route('/api/lance', methods=['POST'])
def enviar_lance():
    data = request.get_json()
    response = gateway_stub.EnviarLance(lance_pb2.EnviarLanceRequest(
        leilao_id=data['leilao_id'],
        user_id=data['user_id'],
        valor=data['valor']
    ))
    return jsonify({'success': response.success})
```

### Frontend: static/app.js

```javascript
const API_URL = 'http://localhost:3000/api';

async function buscarLeiloes() {
    const response = await fetch(`${API_URL}/leiloes`);
    const data = await response.json();
    renderLeiloes(data.leiloes);
}

async function enviarLance(leilaoId, valor) {
    const response = await fetch(`${API_URL}/lance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            leilao_id: leilaoId,
            user_id: sessionStorage.getItem('userId'),
            valor: valor
        })
    });
    const data = await response.json();
    alert(data.success ? 'Lance enviado!' : 'Erro');
}
```

## 🧪 Testando o Sistema

### Opção 1: Interface Web (Recomendado)

1. Inicie todos os serviços
2. Acesse `http://localhost:3000`
3. Use a interface para:
   - Ver leilões ativos
   - Criar novos leilões
   - Registrar interesse
   - Fazer lances

### Opção 2: Cliente Python

```python
import grpc
import gateway_pb2
import gateway_pb2_grpc
import leilao_pb2
import lance_pb2

# Conectar ao Gateway
channel = grpc.insecure_channel('localhost:50054')
stub = gateway_pb2_grpc.GatewayServiceStub(channel)

# 1. Listar leilões
print("=== Leilões Disponíveis ===")
response = stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
for leilao in response.leiloes:
    print(f"{leilao.id}: {leilao.nome} - R$ {leilao.valor_inicial}")

# 2. Registrar interesse
response = stub.RegistrarInteresse(leilao_pb2.RegistrarInteresseRequest(
    leilao_id=1,
    cliente_id="user123"
))
print(f"\n{response.message}")

# 3. Enviar lance
response = stub.EnviarLance(lance_pb2.EnviarLanceRequest(
    leilao_id=1,
    user_id="user123",
    valor=1500.0
))
print(f"Lance: {response.message} (Válido: {response.valido})")

# 4. Receber notificações em tempo real
print("\n=== Aguardando notificações ===")
for notificacao in stub.StreamNotificacoesUnificadas(
    gateway_pb2.StreamNotificacoesUnificadasRequest(cliente_id="user123")
):
    print(f"[{notificacao.tipo}] Leilão {notificacao.leilao_id}")
    if notificacao.tipo == "NOVO_LANCE":
        print(f"  → Lance de R$ {notificacao.valor}")
    elif notificacao.tipo == "VENCEDOR":
        print(f"  → Vencedor: {notificacao.id_vencedor}")
    elif notificacao.tipo == "LINK_PAGAMENTO":
        print(f"  → Pagar em: {notificacao.link_pagamento}")
```

### Opção 3: grpcurl (CLI)

```powershell
# Instalar
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# Listar serviços disponíveis
grpcurl -plaintext localhost:50054 list

# Listar métodos do Gateway
grpcurl -plaintext localhost:50054 list gateway.GatewayService

# Chamar ListarLeiloes
grpcurl -plaintext -d '{}' localhost:50054 gateway.GatewayService/ListarLeiloes

# Enviar lance
grpcurl -plaintext -d '{
  "leilao_id": 1,
  "user_id": "user123",
  "valor": 1500.0
}' localhost:50054 gateway.GatewayService/EnviarLance

# Stream de notificações (mantém conexão aberta)
grpcurl -plaintext -d '{
  "cliente_id": "user123"
}' localhost:50054 gateway.GatewayService/StreamNotificacoesUnificadas
```

### Opção 4: Postman (gRPC)

1. Crie nova requisição **gRPC**
2. URL: `localhost:50054`
3. Selecione método (ex: `gateway.GatewayService/ListarLeiloes`)
4. Envie requisição

## 🎓 Conceitos de Sistemas Distribuídos Aplicados

### 1. **Microsserviços**
- Cada serviço tem responsabilidade única (leilão, lance, pagamento)
- Podem ser escalados independentemente
- Falha isolada (um serviço caindo não derruba todo o sistema)

### 2. **API Gateway Pattern**
- Ponto único de entrada (`app.py`)
- Roteamento de requisições
- Agregação de respostas de múltiplos serviços
- Simplifica cliente (1 conexão ao invés de 3)

### 3. **Event-Driven Architecture**
- Notificações em tempo real via gRPC Streams
- Clientes recebem eventos sem polling
- Comunicação assíncrona entre serviços

### 4. **Service Discovery**
- Serviços conhecem endereços fixos (localhost:5005X)
- Em produção: usar Consul, Eureka, ou Kubernetes Service Discovery

### 5. **Circuit Breaker (Implícito)**
- gRPC tem retry automático
- Timeout configurável
- Pode adicionar exponential backoff

### 6. **Serialização Eficiente**
- Protocol Buffers é 3-10x mais rápido que JSON
- Mensagens menores (binário vs texto)
- Tipo-seguro (erros em tempo de compilação)

### 7. **Comunicação Síncrona e Assíncrona**
- **Síncrona:** Criar leilão, enviar lance (Unary RPC)
- **Assíncrona:** Notificações em tempo real (Server Streaming)

---

## 🚀 Melhorias Possíveis

### 1. Persistência de Dados
```python
# Usar SQLAlchemy + PostgreSQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://user:pass@localhost/leiloes')
Session = sessionmaker(bind=engine)
```

### 2. Autenticação e Autorização
```python
# gRPC Interceptors para validar JWT
class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        token = metadata.get('authorization')
        if not validate_jwt(token):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Token inválido')
        return continuation(handler_call_details)
```

### 3. Service Discovery Dinâmico
```python
# Usar Consul para descobrir serviços
import consul

c = consul.Consul()
services = c.health.service('leilao-service', passing=True)
leilao_addr = f"{services[0]['Service']['Address']}:{services[0]['Service']['Port']}"
```

### 4. Load Balancing
```python
# gRPC tem load balancing nativo
channel = grpc.insecure_channel(
    'dns:///leilao-service:50051',
    options=[('grpc.lb_policy_name', 'round_robin')]
)
```

### 5. Observabilidade
```python
# Adicionar logging estruturado
import structlog
logger = structlog.get_logger()

# Métricas com Prometheus
from prometheus_client import Counter, Histogram

request_count = Counter('grpc_requests_total', 'Total requests')
request_latency = Histogram('grpc_request_duration_seconds', 'Request latency')

# Tracing com OpenTelemetry
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("criar_leilao"):
    # código...
```

### 6. Containerização Completa
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "services/ms_leilao.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  ms_leilao:
    build: .
    command: python services/ms_leilao.py
    ports: ["50051:50051"]
  
  ms_lance:
    build: .
    command: python services/ms_lance.py
    ports: ["50052:50052"]
  
  gateway:
    build: .
    command: python app.py
    ports: ["50054:50054"]
    depends_on: [ms_leilao, ms_lance, ms_pagamento]
```

### 7. Health Checks
```python
# health.proto
service Health {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
}

# Implementação
class HealthServicer(health_pb2_grpc.HealthServicer):
    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING
        )
```

### 8. Rate Limiting
```python
from functools import wraps
import time

def rate_limit(max_calls, period):
    calls = []
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=10, period=60)
def EnviarLance(self, request, context):
    # ...
```

---

## 🔒 Segurança

### 1. TLS/SSL (Produção)
```python
# Servidor com TLS
server_credentials = grpc.ssl_server_credentials(
    [(private_key, certificate_chain)]
)
server.add_secure_port('[::]:50051', server_credentials)

# Cliente com TLS
channel_credentials = grpc.ssl_channel_credentials(root_certificates)
channel = grpc.secure_channel('localhost:50051', channel_credentials)
```

### 2. Validação de Entrada
```python
def EnviarLance(self, request, context):
    if request.valor <= 0:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Valor deve ser positivo")
    if request.leilao_id not in leiloes:
        context.abort(grpc.StatusCode.NOT_FOUND, "Leilão não encontrado")
```

### 3. Timeout
```python
# Cliente com timeout
response = stub.CriarLeilao(request, timeout=5.0)  # 5 segundos
```

---

## 📊 Comparação: REST vs gRPC

| Aspecto              | REST (HTTP/1.1 + JSON) | gRPC (HTTP/2 + Protobuf) |
| -------------------- | ---------------------- | ------------------------ |
| **Performance**      | ⭐⭐⭐                    | ⭐⭐⭐⭐⭐                      |
| **Tamanho Payload**  | Maior (texto)          | Menor (binário)          |
| **Streaming**        | Limitado (SSE)         | Nativo (bidirecional)    |
| **Browser Support**  | ✅ Nativo               | ❌ Precisa proxy          |
| **Tipagem**          | ❌ Schema opcional      | ✅ Schema obrigatório     |
| **Latência**         | ~50ms                  | ~10ms                    |
| **Debugging**        | Fácil (texto)          | Médio (binário)          |
| **Mobile**           | Bom                    | Excelente                |

**Quando usar gRPC:**
- ✅ Comunicação entre microsserviços internos
- ✅ Alto volume de requisições
- ✅ Streaming em tempo real
- ✅ Apps móveis (economia de bateria/dados)

**Quando usar REST:**
- ✅ APIs públicas (compatibilidade)
- ✅ Prototipagem rápida
- ✅ Clientes web simples

## 🐛 Troubleshooting

### ❌ Erro: "No module named 'gateway_pb2'"
**Solução:** Gere os arquivos Python dos .proto:
```powershell
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/*.proto
```

### ❌ Erro: "failed to connect to all addresses"
**Solução:** Verifique se todos os microsserviços estão rodando:
```powershell
netstat -ano | findstr "50051 50052 50053 50054"
```

### ❌ Erro: "StatusCode.UNAVAILABLE"
**Causa:** Serviço não está acessível  
**Solução:** 
1. Verifique se o serviço está rodando
2. Confirme o endereço/porta corretos
3. Desative firewall/antivírus temporariamente

### ❌ Frontend não carrega leilões
**Solução:** 
1. Verifique se `web_server.py` está rodando (porta 3000)
2. Verifique se `app.py` (Gateway) está rodando (porta 50054)
3. Abra console do navegador (F12) e veja erros JavaScript

### ❌ Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução:**
```powershell
pip install flask flask-cors
```

### ❌ Streams não recebem notificações
**Causa:** Cliente não registrou interesse  
**Solução:** Chame `RegistrarInteresse` antes de conectar ao stream

### ❌ Pagamento não processa
**Solução:** Verifique se `services/pagamento.py` está rodando na porta 5001

---

## 📚 Referências e Documentação

### Documentação Oficial
- [gRPC Python](https://grpc.io/docs/languages/python/) - Guia completo Python
- [Protocol Buffers v3](https://developers.google.com/protocol-buffers/docs/proto3) - Sintaxe .proto
- [gRPC Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/) - Conceitos fundamentais
- [gRPC Best Practices](https://grpc.io/docs/guides/performance/) - Performance e boas práticas

### Tutoriais
- [gRPC Basics Python](https://grpc.io/docs/languages/python/basics/)
- [Building Microservices with gRPC](https://grpc.io/docs/guides/microservices/)

### Ferramentas
- [grpcurl](https://github.com/fullstorydev/grpcurl) - CLI para testar gRPC
- [BloomRPC](https://github.com/bloomrpc/bloomrpc) - GUI para testar gRPC (como Postman)
- [grpcui](https://github.com/fullstorydev/grpcui) - Interface web para gRPC

### Livros Recomendados
- "Building Microservices" - Sam Newman
- "gRPC: Up and Running" - Kasun Indrasiri
- "Designing Data-Intensive Applications" - Martin Kleppmann

---

## 👥 Autores e Contribuições

**Desenvolvido como projeto acadêmico para disciplina de Sistemas Distribuídos**

### Estrutura Original
- Backend gRPC com microsserviços
- API Gateway para agregação
- Streaming em tempo real
- Integração com serviço externo

### Melhorias Implementadas
- Interface web Flask
- JavaScript frontend moderno
- Documentação completa
- Exemplos de uso

---

## 📄 Licença

Este projeto é de código aberto para fins educacionais.

---

## 🎯 Próximos Passos

### Para Aprender Mais:
1. ✅ Implementar persistência com PostgreSQL
2. ✅ Adicionar autenticação JWT
3. ✅ Containerizar com Docker
4. ✅ Implementar service discovery com Consul
5. ✅ Adicionar observabilidade (Prometheus + Grafana)
6. ✅ Implementar circuit breaker
7. ✅ Deploy em Kubernetes

### Para Melhorar o Projeto:
1. Adicionar testes unitários (pytest)
2. Testes de integração entre microsserviços
3. CI/CD com GitHub Actions
4. Documentação da API (Swagger/OpenAPI)
5. Interface web mais rica (React/Vue)
6. Notificações push no navegador
7. Sistema de avaliação de vendedores

---

## 📞 Suporte

**Problemas ou dúvidas?**
1. Verifique a seção de Troubleshooting acima
2. Confira os logs dos microsserviços
3. Teste com grpcurl para isolar o problema
4. Abra uma issue no repositório

---

**🚀 Bom estudo de Sistemas Distribuídos!**

### Frontend não conecta

Configure o Envoy Proxy ou grpcwebproxy para fazer a ponte entre HTTP/1.1 e HTTP/2.

## 📄 Licença

Este projeto é um exemplo educacional para demonstrar arquitetura de microsserviços com gRPC.
