import time
import grpc
from concurrent import futures
import threading
from queue import Queue, Empty
import requests
from flask import Flask, request, jsonify
import generated.pagamento_pb2_grpc as pagamento_pb2_grpc
import generated.pagamento_pb2 as pagamento_pb2

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
        
        link_pagamento = None
        id_transacao = None
        
        try:
            resp = requests.post('http://localhost:5001/api/pagamento', json=payload, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            link_pagamento = data.get('link_pagamento')
            id_transacao = data.get('id_transacao')
        except Exception:
            id_transacao = id_transacao or f"tx-{request.leilao_id}-{int(time.time())}"
            link_pagamento = link_pagamento or f"http://pagamento/{id_transacao}"

        publish_message('link_pagamento', {
            'leilao_id': request.leilao_id,
            'cliente_id': request.cliente_id,
            'valor': request.valor,
            'moeda': request.moeda or 'BRL',
            'id_transacao': id_transacao,
            'link_pagamento': link_pagamento
        })
        
        publish_message('status_pagamento', {
            'leilao_id': request.leilao_id,
            'id_transacao': id_transacao,
            'status': 'pendente'
        })

        return pagamento_pb2.ProcessarPagamentoResponse(
            success=True,
            message='Pagamento iniciado',
            id_transacao=id_transacao,
            link_pagamento=link_pagamento
        )
    
    def StreamPagamentos(self, request, context):
        q = Queue(maxsize=100)
        with subs_lock:
            subscribers.add(q)
        try:
            while context.is_active():
                try:
                    notif = q.get(timeout=1)
                    yield notif
                except Empty:
                    continue
        finally:
            with subs_lock:
                subscribers.discard(q)
    
    def NotificarVencedor(self, request, context):
        payload = {
            'leilao_id': request.leilao_id,
            'cliente_id': request.id_vencedor,
            'valor': request.valor,
            'moeda': 'BRL'
        }
        link_pagamento = None
        id_transacao = None
        try:
            resp = requests.post('http://localhost:5001/api/pagamento', json=payload, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            link_pagamento = data.get('link_pagamento')
            id_transacao = data.get('id_transacao')
        except Exception:
            id_transacao = f"tx-{request.leilao_id}-{int(time.time())}"
            link_pagamento = f"http://pagamento/{id_transacao}"

        publish_message('link_pagamento', {
            'leilao_id': request.leilao_id,
            'cliente_id': request.id_vencedor,
            'valor': request.valor,
            'moeda': 'BRL',
            'id_transacao': id_transacao,
            'link_pagamento': link_pagamento
        })
        publish_message('status_pagamento', {
            'leilao_id': request.leilao_id,
            'id_transacao': id_transacao,
            'status': 'pendente'
        })
        return pagamento_pb2.NotificarVencedorResponse(success=True)

def publish_message(event_type, message_dict):
    notif = pagamento_pb2.NotificacaoPagamento(
        tipo=event_type,
        leilao_id=int(message_dict.get('leilao_id', 0) or 0),
        cliente_id=message_dict.get('cliente_id') or None,
        id_transacao=message_dict.get('id_transacao') or None,
        link_pagamento=message_dict.get('link_pagamento') or None,
        status=message_dict.get('status') or None,
        valor=float(message_dict.get('valor', 0.0) or 0.0),
    )
    
    with subs_lock:
        for q in list(subscribers):
            q.put(notif, block=False)

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

    publish_message('status_pagamento', {
        'leilao_id': leilao_id,
        'id_transacao': id_transacao,
        'status': status
    })
    
    return jsonify({'ok': True}), 200

@app.get('/healthz')
def healthz():
    return jsonify({'status': 'ok'})

def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pagamento_pb2_grpc.add_PagamentoServiceServicer_to_server(PagamentoServiceImpl(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print('[Pagamento] gRPC server em :50051')
        server.wait_for_termination()

if __name__ == '__main__':
    t = threading.Thread(target=serve, daemon=True)
    t.start()
    time.sleep(1)
    print('[Pagamento] Servindo webhook em http://127.0.0.1:4446')
    app.run(host='127.0.0.1', port=4446, debug=False, use_reloader=False)