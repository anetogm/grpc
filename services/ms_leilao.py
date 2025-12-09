import grpc
from concurrent import futures
import time
from datetime import datetime, timedelta
import threading
import sys
import os

# Adicionar diretório raiz ao path para importar generated
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import generated.leilao_pb2
import generated.leilao_pb2_grpc
import generated.lance_pb2
import generated.lance_pb2_grpc

inicio = datetime.now() + timedelta(seconds=2)
fim = inicio + timedelta(minutes=2)

leiloes = [
    {
        'id': 1,
        'nome': 'Notebook',
        'descricao': 'Macbook Pro 16" M2 Max assinado pelo Steve Jobs',
        'valor_inicial': 1000,
        'inicio': inicio,
        'fim': fim,
        'status': 'ativo'
    },
    {
        'id': 2,
        'nome': 'celular',
        'descricao': 'Iphone 17 Pro Max Turbo assinado pelo Steve Jobs',
        'valor_inicial': 2000,
        'inicio': inicio,
        'fim': fim,
        'status': 'ativo'
    }
]

lock = threading.Lock()
clientes_interessados = {}  # {leilao_id: set(cliente_ids)}
streams_ativos = {}  # {cliente_id: [queue]}


class LeilaoServicer(generated.leilao_pb2_grpc.LeilaoServiceServicer):
    
    def CriarLeilao(self, request, context):
        try:
            with lock:
                next_id = max((int(l['id']) for l in leiloes), default=0) + 1
            
            try:
                inicio_dt = datetime.fromisoformat(request.inicio) if request.inicio else datetime.now() + timedelta(seconds=2)
            except Exception:
                inicio_dt = datetime.now() + timedelta(seconds=2)
            
            try:
                fim_dt = datetime.fromisoformat(request.fim) if request.fim else inicio_dt + timedelta(minutes=50)
            except Exception:
                fim_dt = inicio_dt + timedelta(minutes=50)
            
            leilao = {
                'id': next_id,
                'nome': request.nome,
                'descricao': request.descricao,
                'valor_inicial': request.valor_inicial,
                'inicio': inicio_dt,
                'fim': fim_dt,
                'status': 'ativo'
            }
            
            with lock:
                leiloes.append(leilao)
            
            # Iniciar gerenciamento do leilão em thread separada
            t = threading.Thread(target=gerenciar_leilao, args=(leilao,), daemon=True)
            t.start()
            
            # Criar resposta
            leilao_pb = generated.leilao_pb2.Leilao(
                id=next_id,
                nome=request.nome,
                descricao=request.descricao,
                valor_inicial=request.valor_inicial,
                inicio=inicio_dt.isoformat(),
                fim=fim_dt.isoformat(),
                status='ativo'
            )
            
            return generated.leilao_pb2.CriarLeilaoResponse(
                success=True,
                message="Leilão cadastrado com sucesso",
                leilao_id=next_id,
                leilao=leilao_pb
            )
        except Exception as e:
            return generated.leilao_pb2.CriarLeilaoResponse(
                success=False,
                message=f"Erro ao criar leilão: {str(e)}"
            )
    
    def ListarLeiloes(self, request, context):
        with lock:
            leiloes_pb = []
            for l in leiloes:
                leilao_pb = generated.leilao_pb2.Leilao(
                    id=l['id'],
                    nome=l['nome'],
                    descricao=l['descricao'],
                    valor_inicial=l['valor_inicial'],
                    inicio=l['inicio'].isoformat() if isinstance(l['inicio'], datetime) else str(l['inicio']),
                    fim=l['fim'].isoformat() if isinstance(l['fim'], datetime) else str(l['fim']),
                    status=l['status']
                )
                leiloes_pb.append(leilao_pb)
        
        return generated.leilao_pb2.ListarLeiloesResponse(leiloes=leiloes_pb)
    
    def RegistrarInteresse(self, request, context):
        leilao_id = request.leilao_id
        cliente_id = request.cliente_id
        
        with lock:
            if leilao_id not in clientes_interessados:
                clientes_interessados[leilao_id] = set()
            clientes_interessados[leilao_id].add(cliente_id)
        
        print(f"[ms_leilao] Cliente {cliente_id} registrou interesse no leilão {leilao_id}")
        
        return generated.leilao_pb2.RegistrarInteresseResponse(
            success=True,
            message="Interesse registrado com sucesso"
        )
    
    def CancelarInteresse(self, request, context):
        leilao_id = request.leilao_id
        cliente_id = request.cliente_id
        
        with lock:
            if leilao_id in clientes_interessados:
                clientes_interessados[leilao_id].discard(cliente_id)
                if len(clientes_interessados[leilao_id]) == 0:
                    del clientes_interessados[leilao_id]
        
        print(f"[ms_leilao] Cliente {cliente_id} cancelou interesse no leilão {leilao_id}")
        
        return generated.leilao_pb2.CancelarInteresseResponse(
            success=True,
            message="Interesse cancelado com sucesso"
        )
    
    def StreamNotificacoes(self, request, context):
        """Stream de notificações para um cliente específico"""
        cliente_id = request.cliente_id
        print(f"[ms_leilao] Cliente {cliente_id} conectado ao stream de notificações")
        
        # Criar fila para este cliente
        import queue
        notification_queue = queue.Queue()
        
        with lock:
            if cliente_id not in streams_ativos:
                streams_ativos[cliente_id] = []
            streams_ativos[cliente_id].append(notification_queue)
        
        try:
            while context.is_active():
                try:
                    # Aguardar notificação com timeout
                    notificacao = notification_queue.get(timeout=1.0)
                    yield notificacao
                except:
                    # Timeout, continuar esperando
                    pass
        finally:
            # Remover fila ao desconectar
            with lock:
                if cliente_id in streams_ativos:
                    streams_ativos[cliente_id].remove(notification_queue)
                    if len(streams_ativos[cliente_id]) == 0:
                        del streams_ativos[cliente_id]
            print(f"[ms_leilao] Cliente {cliente_id} desconectado do stream")


def notificar_clientes_leilao(leilao_id, tipo, leilao_data):
    """Enviar notificação para todos os clientes interessados em um leilão"""
    with lock:
        if leilao_id not in clientes_interessados:
            return
        
        clientes = list(clientes_interessados[leilao_id])
    
    leilao_pb = generated.leilao_pb2.Leilao(
        id=leilao_data['id'],
        nome=leilao_data['nome'],
        descricao=leilao_data['descricao'],
        valor_inicial=leilao_data['valor_inicial'],
        inicio=leilao_data['inicio'].isoformat() if isinstance(leilao_data['inicio'], datetime) else str(leilao_data['inicio']),
        fim=leilao_data['fim'].isoformat() if isinstance(leilao_data['fim'], datetime) else str(leilao_data['fim']),
        status=leilao_data['status']
    )
    
    notificacao = generated.leilao_pb2.NotificacaoLeilao(
        tipo=tipo,
        leilao_id=leilao_id,
        leilao=leilao_pb
    )
    
    with lock:
        for cliente_id in clientes:
            if cliente_id in streams_ativos:
                for queue in streams_ativos[cliente_id]:
                    try:
                        queue.put_nowait(notificacao)
                    except:
                        pass

def gerenciar_leilao(leilao):
    """Gerencia o ciclo de vida de um leilão"""
    leilao_id = leilao['id']
    
    # Aguardar até o início
    tempo_ate_inicio = (leilao['inicio'] - datetime.now()).total_seconds()
    if tempo_ate_inicio > 0:
        time.sleep(tempo_ate_inicio)
    
    leilao['status'] = 'ativo'
    print(f"[ms_leilao] Leilão {leilao_id} iniciado")
    
    # Notificar via gRPC o microsserviço de lances que leilão iniciou
    try:
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = generated.lance_pb2_grpc.LanceServiceStub(channel)
            leilao_ativo = generated.lance_pb2.LeilaoAtivo(
                id=leilao_id,
                nome=leilao['nome'],
                descricao=leilao['descricao'],
                valor_inicial=leilao['valor_inicial'],
                inicio=leilao['inicio'].isoformat(),
                fim=leilao['fim'].isoformat()
            )
            request = generated.lance_pb2.IniciarLeilaoRequest(leilao=leilao_ativo)
            stub.IniciarLeilao(request)
    except Exception as e:
        print(f"[ms_leilao] Erro ao notificar início do leilão: {e}")
    
    # Notificar clientes interessados
    notificar_clientes_leilao(leilao_id, "leilao_iniciado", leilao)
    
    # Aguardar até o fim
    tempo_ate_fim = (leilao['fim'] - datetime.now()).total_seconds()
    if tempo_ate_fim > 0:
        time.sleep(tempo_ate_fim)
    
    leilao['status'] = 'encerrado'
    print(f"[ms_leilao] Leilão {leilao_id} finalizado")
    
    # Notificar via gRPC o microsserviço de lances que leilão finalizou
    try:
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = generated.lance_pb2_grpc.LanceServiceStub(channel)
            request = generated.lance_pb2.FinalizarLeilaoRequest(leilao_id=leilao_id)
            response = stub.FinalizarLeilao(request)
            
            # Se houver vencedor, notificar clientes
            if response.success and response.id_vencedor:
                # Aqui poderíamos notificar o serviço de pagamento
                print(f"[ms_leilao] Vencedor do leilão {leilao_id}: {response.id_vencedor} - R$ {response.valor}")
    except Exception as e:
        print(f"[ms_leilao] Erro ao finalizar leilão: {e}")
    
    # Notificar clientes interessados
    notificar_clientes_leilao(leilao_id, "leilao_finalizado", leilao)


def serve():
    """Iniciar servidor gRPC"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    generated.leilao_pb2_grpc.add_LeilaoServiceServicer_to_server(LeilaoServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("[ms_leilao] Servidor gRPC iniciado na porta 50051")
    
    # Iniciar gerenciamento dos leilões existentes
    for leilao in leiloes:
        t = threading.Thread(target=gerenciar_leilao, args=(leilao,), daemon=True)
        t.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("[ms_leilao] Servidor encerrado")
        server.stop(0)


if __name__ == "__main__":
    print("[ms_leilao] Iniciando servidor gRPC...")
    serve()
 
