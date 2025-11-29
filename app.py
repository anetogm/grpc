import grpc
from concurrent import futures
import threading
import sys
import os

# Adicionar diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

import gateway_pb2
import gateway_pb2_grpc
import leilao_pb2
import leilao_pb2_grpc
import lance_pb2
import lance_pb2_grpc
import pagamento_pb2
import pagamento_pb2_grpc

lock = threading.Lock()
streams_ativos = {}  # {cliente_id: [queue]}

# Endereços dos microsserviços
LEILAO_SERVICE = 'localhost:50051'
LANCE_SERVICE = 'localhost:50052'
PAGAMENTO_SERVICE = 'localhost:50053'


class GatewayServicer(gateway_pb2_grpc.GatewayServiceServicer):
    """API Gateway que agrega todos os microsserviços"""
    
    def __init__(self):
        # Criar conexões persistentes com os microsserviços
        self.leilao_channel = grpc.insecure_channel(LEILAO_SERVICE)
        self.lance_channel = grpc.insecure_channel(LANCE_SERVICE)
        self.pagamento_channel = grpc.insecure_channel(PAGAMENTO_SERVICE)
        
        self.leilao_stub = leilao_pb2_grpc.LeilaoServiceStub(self.leilao_channel)
        self.lance_stub = lance_pb2_grpc.LanceServiceStub(self.lance_channel)
        self.pagamento_stub = pagamento_pb2_grpc.PagamentoServiceStub(self.pagamento_channel)
        
        print("[Gateway] Conexões com microsserviços estabelecidas")
    
    # ========== MÉTODOS DE LEILÃO ==========
    
    def CriarLeilao(self, request, context):
        """Criar novo leilão"""
        try:
            response = self.leilao_stub.CriarLeilao(request)
            return response
        except Exception as e:
            print(f"[Gateway] Erro ao criar leilão: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return leilao_pb2.CriarLeilaoResponse(success=False, message=str(e))
    
    def ListarLeiloes(self, request, context):
        """Listar todos os leilões"""
        try:
            response = self.leilao_stub.ListarLeiloes(request)
            return response
        except Exception as e:
            print(f"[Gateway] Erro ao listar leilões: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return leilao_pb2.ListarLeiloesResponse(leiloes=[])
    
    def RegistrarInteresse(self, request, context):
        """Registrar interesse em um leilão"""
        try:
            response = self.leilao_stub.RegistrarInteresse(request)
            return response
        except Exception as e:
            print(f"[Gateway] Erro ao registrar interesse: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return leilao_pb2.RegistrarInteresseResponse(success=False, message=str(e))
    
    def CancelarInteresse(self, request, context):
        """Cancelar interesse em um leilão"""
        try:
            response = self.leilao_stub.CancelarInteresse(request)
            return response
        except Exception as e:
            print(f"[Gateway] Erro ao cancelar interesse: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return leilao_pb2.CancelarInteresseResponse(success=False, message=str(e))
    
    # ========== MÉTODOS DE LANCE ==========
    
    def EnviarLance(self, request, context):
        """Enviar um lance"""
        try:
            response = self.lance_stub.EnviarLance(request)
            return response
        except Exception as e:
            print(f"[Gateway] Erro ao enviar lance: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return lance_pb2.EnviarLanceResponse(success=False, message=str(e), valido=False)
    
    # ========== MÉTODOS DE PAGAMENTO ==========
    
    def ProcessarPagamento(self, request, context):
        """Processar pagamento"""
        try:
            response = self.pagamento_stub.ProcessarPagamento(request)
            return response
        except Exception as e:
            print(f"[Gateway] Erro ao processar pagamento: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pagamento_pb2.ProcessarPagamentoResponse(success=False, message=str(e))
    
    # ========== STREAM UNIFICADO DE NOTIFICAÇÕES ==========
    
    def StreamNotificacoesUnificadas(self, request, context):
        """Stream unificado de todas as notificações para um cliente"""
        cliente_id = request.cliente_id
        print(f"[Gateway] Cliente {cliente_id} conectado ao stream unificado")
        
        import queue
        notification_queue = queue.Queue()
        
        with lock:
            if cliente_id not in streams_ativos:
                streams_ativos[cliente_id] = []
            streams_ativos[cliente_id].append(notification_queue)
        
        # Iniciar threads para receber notificações dos microsserviços
        stop_event = threading.Event()
        
        def forward_leilao_notifications():
            """Receber e encaminhar notificações de leilão"""
            try:
                req = leilao_pb2.StreamNotificacoesRequest(cliente_id=cliente_id)
                for notif in self.leilao_stub.StreamNotificacoes(req):
                    if stop_event.is_set():
                        break
                    # Converter para notificação unificada
                    unified = gateway_pb2.NotificacaoUnificada(
                        tipo=notif.tipo,
                        leilao_id=notif.leilao_id,
                        leilao=notif.leilao
                    )
                    notification_queue.put(unified)
            except Exception as e:
                print(f"[Gateway] Erro no stream de leilão: {e}")
        
        def forward_lance_notifications():
            """Receber e encaminhar notificações de lance"""
            try:
                req = lance_pb2.StreamLancesRequest(cliente_id=cliente_id)
                for notif in self.lance_stub.StreamLances(req):
                    if stop_event.is_set():
                        break
                    # Converter para notificação unificada
                    unified = gateway_pb2.NotificacaoUnificada(
                        tipo=notif.tipo,
                        leilao_id=notif.leilao_id,
                        user_id=notif.user_id,
                        valor=notif.valor,
                        id_vencedor=notif.id_vencedor
                    )
                    notification_queue.put(unified)
            except Exception as e:
                print(f"[Gateway] Erro no stream de lance: {e}")
        
        def forward_pagamento_notifications():
            """Receber e encaminhar notificações de pagamento"""
            try:
                req = pagamento_pb2.StreamPagamentosRequest(cliente_id=cliente_id)
                for notif in self.pagamento_stub.StreamPagamentos(req):
                    if stop_event.is_set():
                        break
                    # Converter para notificação unificada
                    unified = gateway_pb2.NotificacaoUnificada(
                        tipo=notif.tipo,
                        leilao_id=notif.leilao_id,
                        user_id=notif.cliente_id,
                        valor=notif.valor,
                        link_pagamento=notif.link_pagamento,
                        status=notif.status
                    )
                    notification_queue.put(unified)
            except Exception as e:
                print(f"[Gateway] Erro no stream de pagamento: {e}")
        
        # Iniciar threads de forward
        threads = [
            threading.Thread(target=forward_leilao_notifications, daemon=True),
            threading.Thread(target=forward_lance_notifications, daemon=True),
            threading.Thread(target=forward_pagamento_notifications, daemon=True)
        ]
        
        for t in threads:
            t.start()
        
        # Enviar notificações ao cliente
        try:
            while context.is_active():
                try:
                    notificacao = notification_queue.get(timeout=1.0)
                    yield notificacao
                except:
                    pass
        finally:
            # Limpar ao desconectar
            stop_event.set()
            with lock:
                if cliente_id in streams_ativos:
                    streams_ativos[cliente_id].remove(notification_queue)
                    if len(streams_ativos[cliente_id]) == 0:
                        del streams_ativos[cliente_id]
            print(f"[Gateway] Cliente {cliente_id} desconectado do stream unificado")


def serve():
    """Iniciar API Gateway gRPC"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gateway_pb2_grpc.add_GatewayServiceServicer_to_server(GatewayServicer(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("[Gateway] API Gateway gRPC iniciado na porta 50054")
    print("[Gateway] Conectado aos microsserviços:")
    print(f"  - Leilão: {LEILAO_SERVICE}")
    print(f"  - Lance: {LANCE_SERVICE}")
    print(f"  - Pagamento: {PAGAMENTO_SERVICE}")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("[Gateway] Servidor encerrado")
        server.stop(0)


if __name__ == "__main__":
    print("[Gateway] Iniciando API Gateway gRPC...")
    serve()
