import grpc
from concurrent import futures
import threading
import time
import requests
import sys
import os

# Adicionar diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generated'))

import pagamento_pb2
import pagamento_pb2_grpc

lock = threading.Lock()
streams_ativos = {}  # {cliente_id: [queue]}


class PagamentoServicer(pagamento_pb2_grpc.PagamentoServiceServicer):
    
    def NotificarVencedor(self, request, context):
        """Recebe notificação de vencedor e inicia processo de pagamento"""
        leilao_id = request.leilao_id
        id_vencedor = request.id_vencedor
        valor = request.valor
        
        print(f'[Pagamento] Vencedor notificado: Leilão {leilao_id}, Cliente {id_vencedor}, Valor R$ {valor}')
        
        # Fazer requisição para serviço externo de pagamento
        payload = {
            'leilao_id': leilao_id,
            'cliente_id': id_vencedor,
            'valor': valor,
            'moeda': 'BRL'
        }
        
        url_externo = 'http://localhost:5001/api/pagamento'
        link_pagamento = None
        id_transacao = None
        
        try:
            resp = requests.post(url_externo, json=payload, timeout=5)
            resp.raise_for_status()
            retorno = resp.json()
            link_pagamento = retorno.get('link_pagamento')
            id_transacao = retorno.get('id_transacao')
            print(f"[Pagamento] Resposta externa: {retorno}")
        except Exception as e:
            print(f"[Pagamento] Falha na chamada externa, usando fallback: {e}")
        
        # Fallback se serviço externo falhar
        if not link_pagamento:
            id_transacao = id_transacao or f"tx-{leilao_id}-{int(time.time())}"
            link_pagamento = f"http://pagamento/{id_transacao}"
            print('[Pagamento] Link de pagamento gerado via fallback.')
        
        # Notificar cliente sobre link de pagamento
        notificar_link_pagamento(leilao_id, id_vencedor, id_transacao, link_pagamento, valor)
        
        # Notificar cliente sobre status inicial
        notificar_status_pagamento(leilao_id, id_vencedor, id_transacao, 'pendente', valor)
        
        return pagamento_pb2.NotificarVencedorResponse(success=True)
    
    def ProcessarPagamento(self, request, context):
        """Processar pagamento (webhook ou chamada direta)"""
        leilao_id = request.leilao_id
        cliente_id = request.cliente_id
        valor = request.valor
        moeda = request.moeda or 'BRL'
        
        # Gerar transação
        id_transacao = f"tx-{leilao_id}-{int(time.time())}"
        link_pagamento = f"http://pagamento/{id_transacao}"
        
        # Notificar cliente
        notificar_link_pagamento(leilao_id, cliente_id, id_transacao, link_pagamento, valor)
        
        return pagamento_pb2.ProcessarPagamentoResponse(
            success=True,
            message='Pagamento iniciado',
            id_transacao=id_transacao,
            link_pagamento=link_pagamento
        )
    
    def StreamPagamentos(self, request, context):
        """Stream de notificações de pagamento para um cliente"""
        cliente_id = request.cliente_id
        print(f"[Pagamento] Cliente {cliente_id} conectado ao stream de pagamentos")
        
        import queue
        notification_queue = queue.Queue()
        
        with lock:
            if cliente_id not in streams_ativos:
                streams_ativos[cliente_id] = []
            streams_ativos[cliente_id].append(notification_queue)
        
        try:
            while context.is_active():
                try:
                    notificacao = notification_queue.get(timeout=1.0)
                    yield notificacao
                except:
                    pass
        finally:
            with lock:
                if cliente_id in streams_ativos:
                    streams_ativos[cliente_id].remove(notification_queue)
                    if len(streams_ativos[cliente_id]) == 0:
                        del streams_ativos[cliente_id]
            print(f"[Pagamento] Cliente {cliente_id} desconectado do stream")


def notificar_link_pagamento(leilao_id, cliente_id, id_transacao, link_pagamento, valor):
    """Notificar cliente sobre link de pagamento"""
    notificacao = pagamento_pb2.NotificacaoPagamento(
        tipo='link_pagamento',
        leilao_id=leilao_id,
        cliente_id=cliente_id,
        id_transacao=id_transacao,
        link_pagamento=link_pagamento,
        valor=valor
    )
    
    with lock:
        if cliente_id in streams_ativos:
            for queue in streams_ativos[cliente_id]:
                try:
                    queue.put_nowait(notificacao)
                except:
                    pass
    
    print(f"[Pagamento] Link enviado ao cliente {cliente_id}: {link_pagamento}")


def notificar_status_pagamento(leilao_id, cliente_id, id_transacao, status, valor):
    """Notificar cliente sobre status do pagamento"""
    notificacao = pagamento_pb2.NotificacaoPagamento(
        tipo='status_pagamento',
        leilao_id=leilao_id,
        cliente_id=cliente_id,
        id_transacao=id_transacao,
        status=status,
        valor=valor
    )
    
    with lock:
        if cliente_id in streams_ativos:
            for queue in streams_ativos[cliente_id]:
                try:
                    queue.put_nowait(notificacao)
                except:
                    pass
    
    print(f"[Pagamento] Status enviado ao cliente {cliente_id}: {status}")


def serve():
    """Iniciar servidor gRPC"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pagamento_pb2_grpc.add_PagamentoServiceServicer_to_server(PagamentoServicer(), server)
    server.add_insecure_port('0.0.0.0:50053')
    server.start()
    print("[ms_pagamento] Servidor gRPC iniciado na porta 50053")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("[ms_pagamento] Servidor encerrado")
        server.stop(0)


if __name__ == '__main__':
    print("[ms_pagamento] Iniciando servidor gRPC...")
    serve()