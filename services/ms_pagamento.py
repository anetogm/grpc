import time
import grpc
from concurrent import futures
import threading
from queue import Queue, Empty
import requests
from flask import Flask, request, jsonify
import generated.pagamento_pb2_grpc as pagamento_pb2_grpc
import generated.pagamento_pb2 as pagamento_pb2
import generated.api_pb2 as api_pb2
import generated.api_pb2_grpc as api_pb2_grpc

subscribers = set()
subs_lock = threading.Lock()
class PagamentoServiceImpl (pagamento_pb2_grpc.PagamentoServiceServicer):
    def ProcessarPagamento(self, request, context):
        payload = {
            'leilao_id': request.leilao_id,
            'cliente_id': request.cliente_id,
            'valor': request.valor,
            'moeda': request.moeda or 'BRL'
        }
        
        resp = requests.post('http://localhost:5001/api/pagamento', json=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        link_pagamento = data.get('link_pagamento')
        id_transacao = data.get('id_transacao')

        return pagamento_pb2.ProcessarPagamentoResponse(
        success=True,
        message='Pagamento iniciado',
        id_transacao=id_transacao,
        link_pagamento=link_pagamento
        )


app = Flask(__name__)

@app.post('/webhook/pagamento')
def webhook_pagamento():
    body = request.get_json(force=True, silent=False)
    
    id_transacao = body.get('id_transacao')
    leilao_id = body.get('leilao_id')
    status = body.get('status')
    
    if not id_transacao or leilao_id is None:
        return jsonify({'error': 'id_transacao e leilao_id são obrigatórios'}), 400
    
    if status not in ('aprovada', 'recusada', 'pendente'):
        return jsonify({'error': 'status inválido'}), 400

    
    return jsonify({'ok': True}), 200

@app.get('/healthz')
def healthz():
    return jsonify({'status': 'ok'})

def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pagamento_pb2_grpc.add_PagamentoServiceServicer_to_server(PagamentoServiceImpl(), server)
        server.add_insecure_port('[::]:50053')
        server.start()
        print('[Pagamento] gRPC server em :50053')
        server.wait_for_termination()

if __name__ == '__main__':
    t = threading.Thread(target=serve, daemon=True)
    t.start()
    time.sleep(1)
    print('[Pagamento] Servindo webhook em http://127.0.0.1:4446')
    app.run(host='127.0.0.1', port=4446, debug=False, use_reloader=False)