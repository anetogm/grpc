# 📁 Estrutura do Projeto Migrado

```
grpc/
│
├── 📄 app.py                    # API Gateway gRPC (porta 50054)
├── 📄 requirements.txt          # Dependências atualizadas (grpcio, grpcio-tools, protobuf)
│
├── 📂 protos/                   # Definições Protocol Buffers
│   ├── leilao.proto            # Serviço de leilões
│   ├── lance.proto             # Serviço de lances
│   ├── pagamento.proto         # Serviço de pagamentos
│   └── gateway.proto           # API Gateway unificado
│
├── 📂 generated/                # Código Python gerado (criar via grpc_tools)
│   ├── __init__.py
│   ├── leilao_pb2.py
│   ├── leilao_pb2_grpc.py
│   ├── lance_pb2.py
│   ├── lance_pb2_grpc.py
│   ├── pagamento_pb2.py
│   ├── pagamento_pb2_grpc.py
│   ├── gateway_pb2.py
│   └── gateway_pb2_grpc.py
│
├── 📂 services/                 # Microsserviços gRPC
│   ├── ms_leilao.py            # Servidor gRPC (porta 50051)
│   ├── ms_lance.py             # Servidor gRPC (porta 50052)
│   ├── ms_pagamento.py         # Servidor gRPC (porta 50053)
│   └── pagamento.py            # Serviço externo REST (porta 5001)
│
├── 📂 static/                   # Frontend (PENDENTE DE MIGRAÇÃO)
│   ├── script.js               # ⚠️ Usa REST/SSE - precisa ser adaptado
│   └── pagamento.js            # ⚠️ Usa REST - precisa ser adaptado
│
├── 📂 templates/                # Templates HTML
│   ├── index.html
│   ├── cadastra_leilao.html
│   ├── lance.html
│   └── pagar.html
│
├── 📄 generate_grpc.py          # Script para gerar código dos .proto
├── 📄 test_grpc.py              # Script de teste dos serviços
├── 📄 exemplos.py               # Exemplos de uso interativos
│
└── 📚 DOCUMENTAÇÃO
    ├── README.md                # Documentação principal
    ├── SETUP.md                 # Instruções de configuração
    ├── FRONTEND.md              # Guia para migração do frontend
    ├── MIGRACAO.md              # Detalhes da migração
    └── INICIO_RAPIDO.md         # Guia de início rápido
```

## 📊 Mapa de Portas

| Serviço | Porta | Protocolo | Status |
|---------|-------|-----------|--------|
| ms_leilao | 50051 | gRPC | ✅ Implementado |
| ms_lance | 50052 | gRPC | ✅ Implementado |
| ms_pagamento | 50053 | gRPC | ✅ Implementado |
| API Gateway | 50054 | gRPC | ✅ Implementado |
| Serv. Externo | 5001 | HTTP/REST | ✅ Mantido |
| Envoy Proxy | 8080 | HTTP/gRPC-Web | ⏳ Opcional |

## 🔄 Fluxo de Dados

```
┌──────────────────────────────────────────────────────────────┐
│                         Frontend                              │
│                    (JavaScript + gRPC-Web)                    │
│                    ⚠️ Pendente de Migração                     │
└───────────────────────────┬──────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │  Envoy Proxy   │ (opcional)
                    │  localhost:8080│
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │  API Gateway   │
                    │ localhost:50054│
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼───────┐  ┌───────▼────────┐
│  ms_leilao     │  │  ms_lance    │  │  ms_pagamento  │
│ localhost:50051│  │localhost:50052│  │ localhost:50053│
└───────┬────────┘  └──────┬───────┘  └───────┬────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    (Comunicação gRPC)
                            │
                    ┌───────▼────────┐
                    │ Serv. Externo  │
                    │ localhost:5001 │ (HTTP/REST)
                    └────────────────┘
```

## 📝 Arquivos por Categoria

### ✅ Implementados e Funcionando

- `protos/*.proto` - Contratos gRPC
- `services/ms_leilao.py` - Microsserviço refatorado
- `services/ms_lance.py` - Microsserviço refatorado
- `services/ms_pagamento.py` - Microsserviço refatorado
- `app.py` - API Gateway
- `requirements.txt` - Dependências
- `test_grpc.py` - Testes
- `exemplos.py` - Exemplos de uso
- `generate_grpc.py` - Gerador de código
- Toda a documentação (*.md)

### ⚠️ Pendentes de Adaptação

- `static/script.js` - Usa fetch() REST
- `static/pagamento.js` - Usa fetch() REST
- `templates/*.html` - Podem ser mantidos

### ♻️ Mantidos sem Alteração

- `services/pagamento.py` - Serviço externo REST

## 🎯 Comandos Essenciais

### 1. Gerar código dos .proto
```powershell
python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/leilao.proto ./protos/lance.proto ./protos/pagamento.proto ./protos/gateway.proto
```

### 2. Iniciar todos os serviços
```powershell
# 4 terminais separados
python services/ms_leilao.py
python services/ms_lance.py
python services/ms_pagamento.py
python app.py
```

### 3. Testar
```powershell
python test_grpc.py        # Teste automatizado
python exemplos.py         # Menu interativo
```

## 📦 Dependências

### Antes (8 bibliotecas)
```
flask
flask-cors
flask-sse
pika
redis
requests
grpcio
grpcio-tools
```

### Depois (3 bibliotecas + 1 opcional)
```
grpcio==1.60.0
grpcio-tools==1.60.0
protobuf==4.25.1
requests==2.31.0  # Apenas para serviço externo
```

## 🔍 Como Navegar no Projeto

1. **Quero entender o sistema** → Leia `README.md`
2. **Quero começar rápido** → Leia `INICIO_RAPIDO.md`
3. **Quero instalar** → Leia `SETUP.md`
4. **Quero migrar o frontend** → Leia `FRONTEND.md`
5. **Quero detalhes da migração** → Leia `MIGRACAO.md`
6. **Quero ver exemplos** → Execute `python exemplos.py`
7. **Quero testar** → Execute `python test_grpc.py`

## 🏆 Conquistas da Migração

✅ Removido RabbitMQ (mensageria)  
✅ Removido Redis (estado)  
✅ Removido Flask (web framework)  
✅ Removido SSE (notificações)  
✅ Implementado gRPC puro  
✅ Implementado gRPC Streaming  
✅ API Gateway unificado  
✅ Documentação completa  
✅ Scripts de teste  
⏳ Frontend pendente  

---

**Versão**: 1.0  
**Data**: 29/11/2025  
**Status**: Backend Completo | Frontend Pendente  
