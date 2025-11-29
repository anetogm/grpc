import grpc
from concurrent import futures
import threading
import sys
import os
from datetime import datetime

# Adicionar diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generated'))

import lance_pb2
import lance_pb2_grpc
import pagamento_pb2
import pagamento_pb2_grpc

lock = threading.Lock()

leiloes_ativos = {}
lances_atuais = {}
streams_ativos = {}  # {cliente_id: [queue]}


class LanceServicer(lance_pb2_grpc.LanceServiceServicer):
    
    def IniciarLeilao(self, request, context):
        """Recebe notificação de leilão iniciado"""
        leilao = request.leilao
        leilao_id = leilao.id
        
        with lock:
            leiloes_ativos[leilao_id] = {
                'id': leilao.id,
                'nome': leilao.nome,
                'descricao': leilao.descricao,
                'valor_inicial': leilao.valor_inicial,
                'inicio': leilao.inicio,
                'fim': leilao.fim
            }
            print(f"[ms_lance] Leilão {leilao_id} adicionado aos ativos: {leiloes_ativos}")
        
        return lance_pb2.IniciarLeilaoResponse(success=True)
    
    def FinalizarLeilao(self, request, context):
        """Recebe notificação de leilão finalizado"""
        leilao_id = request.leilao_id
        
        with lock:
            leiloes_ativos.pop(leilao_id, None)
            vencedor = lances_atuais.pop(leilao_id, None)
        
        if vencedor:
            print(f"[ms_lance] Vencedor do leilão {leilao_id}: {vencedor['id_cliente']} - R$ {vencedor['valor']}")
            
            # Notificar todos os clientes sobre o vencedor
            notificar_vencedor(leilao_id, vencedor['id_cliente'], vencedor['valor'])
            
            # Notificar serviço de pagamento
            try:
                with grpc.insecure_channel('localhost:50053') as channel:
                    stub = pagamento_pb2_grpc.PagamentoServiceStub(channel)
                    request = pagamento_pb2.NotificarVencedorRequest(
                        leilao_id=leilao_id,
                        id_vencedor=vencedor['id_cliente'],
                        valor=vencedor['valor']
                    )
                    stub.NotificarVencedor(request)
            except Exception as e:
                print(f"[ms_lance] Erro ao notificar pagamento: {e}")
            
            return lance_pb2.FinalizarLeilaoResponse(
                success=True,
                id_vencedor=vencedor['id_cliente'],
                valor=vencedor['valor']
            )
        
        return lance_pb2.FinalizarLeilaoResponse(success=False)
    
    def EnviarLance(self, request, context):
        """Recebe e valida um lance"""
        leilao_id = request.leilao_id
        user_id = request.user_id
        valor = request.valor
        
        with lock:
            # Verificar se leilão está ativo
            if leilao_id not in leiloes_ativos:
                notificar_lance_invalido(user_id, leilao_id, valor)
                return lance_pb2.EnviarLanceResponse(
                    success=False,
                    message='Leilão não está ativo',
                    valido=False
                )
            
            # Verificar se lance é maior que o atual
            lance_atual = lances_atuais.get(leilao_id)
            if lance_atual and valor <= lance_atual['valor']:
                notificar_lance_invalido(user_id, leilao_id, valor)
                return lance_pb2.EnviarLanceResponse(
                    success=False,
                    message='Lance deve ser maior que o atual',
                    valido=False
                )
            
            # Lance válido
            lances_atuais[leilao_id] = {'id_cliente': user_id, 'valor': valor}
            print(f"[ms_lance] Lance válido: Leilão {leilao_id}, Cliente {user_id}, Valor R$ {valor}")
        
        # Notificar todos os clientes interessados
        notificar_lance_valido(leilao_id, user_id, valor)
        
        return lance_pb2.EnviarLanceResponse(
            success=True,
            message='Lance validado com sucesso',
            valido=True
        )
    
    def StreamLances(self, request, context):
        """Stream de notificações de lances para um cliente"""
        cliente_id = request.cliente_id
        print(f"[ms_lance] Cliente {cliente_id} conectado ao stream de lances")
        
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
            print(f"[ms_lance] Cliente {cliente_id} desconectado do stream")


def notificar_lance_valido(leilao_id, user_id, valor):
    """Notificar todos os clientes sobre um lance válido"""
    notificacao = lance_pb2.NotificacaoLance(
        tipo='novo_lance_valido',
        leilao_id=leilao_id,
        user_id=user_id,
        valor=valor
    )
    
    with lock:
        for cliente_id in streams_ativos:
            for queue in streams_ativos[cliente_id]:
                try:
                    queue.put_nowait(notificacao)
                except:
                    pass


def notificar_lance_invalido(user_id, leilao_id, valor):
    """Notificar cliente específico sobre lance inválido"""
    notificacao = lance_pb2.NotificacaoLance(
        tipo='lance_invalido',
        leilao_id=leilao_id,
        user_id=user_id,
        valor=valor
    )
    
    with lock:
        if user_id in streams_ativos:
            for queue in streams_ativos[user_id]:
                try:
                    queue.put_nowait(notificacao)
                except:
                    pass


def notificar_vencedor(leilao_id, id_vencedor, valor):
    """Notificar todos os clientes sobre o vencedor"""
    notificacao = lance_pb2.NotificacaoLance(
        tipo='vencedor_leilao',
        leilao_id=leilao_id,
        id_vencedor=id_vencedor,
        valor=valor
    )
    
    with lock:
        for cliente_id in streams_ativos:
            for queue in streams_ativos[cliente_id]:
                try:
                    queue.put_nowait(notificacao)
                except:
                    pass


def serve():
    """Iniciar servidor gRPC"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lance_pb2_grpc.add_LanceServiceServicer_to_server(LanceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("[ms_lance] Servidor gRPC iniciado na porta 50052")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("[ms_lance] Servidor encerrado")
        server.stop(0)


if __name__ == "__main__":
    print("[ms_lance] Iniciando servidor gRPC...")
    serve()