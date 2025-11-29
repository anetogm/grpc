# Frontend com gRPC-Web - Implementação Pendente

## Status Atual

O backend foi **completamente migrado para gRPC**, mas o frontend ainda precisa ser adaptado. Os arquivos HTML/JavaScript atuais (`static/` e `templates/`) usam REST e SSE, que foram removidos.

## Opções para Implementação do Frontend

### Opção 1: gRPC-Web com Envoy (Recomendado para Produção)

#### Passo 1: Instalar gRPC-Web
```bash
npm install grpc-web
```

#### Passo 2: Gerar stubs JavaScript
```bash
protoc -I=./protos leilao.proto lance.proto pagamento.proto gateway.proto \
  --js_out=import_style=commonjs:./static/generated \
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:./static/generated
```

#### Passo 3: Configurar Envoy
Criar `envoy.yaml`:
```yaml
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
                          route:
                            cluster: gateway_service
                      cors:
                        allow_origin_string_match:
                          - prefix: "*"
                        allow_methods: GET, POST, OPTIONS
                        allow_headers: "*"
                        expose_headers: "*"
                http_filters:
                  - name: envoy.filters.http.grpc_web
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.grpc_web.v3.GrpcWeb
                  - name: envoy.filters.http.cors
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.cors.v3.Cors
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router

  clusters:
    - name: gateway_service
      connect_timeout: 1s
      type: LOGICAL_DNS
      lb_policy: ROUND_ROBIN
      http2_protocol_options: {}
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

Executar Envoy:
```powershell
docker run -d -p 8080:8080 -v ${PWD}/envoy.yaml:/etc/envoy/envoy.yaml:ro envoyproxy/envoy:v1.28-latest
```

#### Passo 4: Código JavaScript
```javascript
const {GatewayServiceClient} = require('./static/generated/gateway_grpc_web_pb');
const {ListarLeiloesRequest, RegistrarInteresseRequest, StreamNotificacoesUnificadasRequest} = require('./static/generated/leilao_pb');

// Conectar ao Envoy
const client = new GatewayServiceClient('http://localhost:8080');

// Listar leilões
const request = new ListarLeiloesRequest();
client.listarLeiloes(request, {}, (err, response) => {
  if (err) {
    console.error(err);
  } else {
    response.getLeiloesList().forEach(leilao => {
      console.log(`${leilao.getId()}: ${leilao.getNome()}`);
    });
  }
});

// Stream de notificações
const streamRequest = new StreamNotificacoesUnificadasRequest();
streamRequest.setClienteId('user123');

const stream = client.streamNotificacoesUnificadas(streamRequest, {});
stream.on('data', (notificacao) => {
  console.log('Notificação:', notificacao.getTipo());
});
stream.on('error', (err) => {
  console.error('Erro no stream:', err);
});
stream.on('end', () => {
  console.log('Stream finalizado');
});
```

---

### Opção 2: grpcwebproxy (Mais Simples, para Desenvolvimento)

#### Instalar:
```bash
go install github.com/improbable-eng/grpc-web/go/grpcwebproxy@latest
```

#### Executar:
```powershell
grpcwebproxy --backend_addr=localhost:50054 --run_tls_server=false --allow_all_origins --server_http_max_read_timeout=10m
```

Usar o mesmo código JavaScript do Opção 1, mas conectando em `http://localhost:8080`.

---

### Opção 3: Servidor Flask Simples como Bridge (Temporário)

Criar um servidor Flask que faz bridge entre REST e gRPC:

```python
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import grpc
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))
import gateway_pb2
import gateway_pb2_grpc
import leilao_pb2
import lance_pb2

app = Flask(__name__)
CORS(app)

# Conectar ao Gateway gRPC
channel = grpc.insecure_channel('localhost:50054')
gateway_stub = gateway_pb2_grpc.GatewayServiceStub(channel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/leiloes', methods=['GET'])
def get_leiloes():
    response = gateway_stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
    leiloes = []
    for leilao in response.leiloes:
        leiloes.append({
            'id': leilao.id,
            'nome': leilao.nome,
            'descricao': leilao.descricao,
            'valor_inicial': leilao.valor_inicial,
            'status': leilao.status
        })
    return jsonify(leiloes)

@app.route('/api/lance', methods=['POST'])
def enviar_lance():
    data = request.json
    response = gateway_stub.EnviarLance(lance_pb2.EnviarLanceRequest(
        leilao_id=data['leilao_id'],
        user_id=data['user_id'],
        valor=data['valor']
    ))
    return jsonify({
        'success': response.success,
        'message': response.message,
        'valido': response.valido
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Manter os arquivos `static/` e `templates/` atuais, mas trocar as URLs para apontar para este bridge.

---

## Recomendação

Para um projeto de produção, use **Opção 1 (Envoy)**.  
Para desenvolvimento rápido, use **Opção 3 (Flask Bridge)**.  
Para aprendizado de gRPC-Web, use **Opção 2 (grpcwebproxy)**.

## Próximos Passos

1. Escolher uma opção
2. Seguir os passos de implementação
3. Adaptar os arquivos JavaScript em `static/`
4. Testar a integração completa

## Recursos

- [gRPC-Web GitHub](https://github.com/grpc/grpc-web)
- [Envoy gRPC-Web Filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/grpc_web_filter)
- [grpcwebproxy](https://github.com/improbable-eng/grpc-web/tree/master/go/grpcwebproxy)
