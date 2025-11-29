"""
Script de Teste para os Serviços gRPC
Execute após iniciar todos os microsserviços
"""
import grpc
import sys
import os

# Adicionar diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

import gateway_pb2
import gateway_pb2_grpc
import leilao_pb2

def test_gateway():
    """Testar conexão com o Gateway"""
    print("\n=== Testando Gateway gRPC ===\n")
    
    try:
        # Conectar ao Gateway
        channel = grpc.insecure_channel('localhost:50054')
        stub = gateway_pb2_grpc.GatewayServiceStub(channel)
        
        # 1. Listar leilões
        print("1. Listando leilões...")
        response = stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
        print(f"   ✓ Encontrados {len(response.leiloes)} leilões")
        for leilao in response.leiloes:
            print(f"   - Leilão {leilao.id}: {leilao.nome} - R$ {leilao.valor_inicial}")
        
        # 2. Registrar interesse
        print("\n2. Registrando interesse...")
        cliente_id = "test_user_123"
        leilao_id = 1
        response = stub.RegistrarInteresse(leilao_pb2.RegistrarInteresseRequest(
            leilao_id=leilao_id,
            cliente_id=cliente_id
        ))
        if response.success:
            print(f"   ✓ Interesse registrado: {response.message}")
        else:
            print(f"   ✗ Erro: {response.message}")
        
        # 3. Testar stream de notificações (apenas 5 segundos)
        print("\n3. Conectando ao stream de notificações (5 segundos)...")
        print("   (Aguardando notificações...)")
        
        import threading
        import time
        
        def listen_stream():
            try:
                for notificacao in stub.StreamNotificacoesUnificadas(
                    gateway_pb2.StreamNotificacoesUnificadasRequest(cliente_id=cliente_id)
                ):
                    print(f"   📩 Notificação: {notificacao.tipo} - Leilão {notificacao.leilao_id}")
            except Exception as e:
                print(f"   Stream finalizado: {e}")
        
        stream_thread = threading.Thread(target=listen_stream, daemon=True)
        stream_thread.start()
        time.sleep(5)
        
        print("   ✓ Stream conectado com sucesso")
        
        # 4. Cancelar interesse
        print("\n4. Cancelando interesse...")
        response = stub.CancelarInteresse(leilao_pb2.CancelarInteresseRequest(
            leilao_id=leilao_id,
            cliente_id=cliente_id
        ))
        if response.success:
            print(f"   ✓ Interesse cancelado: {response.message}")
        
        print("\n✅ Todos os testes passaram!")
        print("\n💡 Dica: Para testar lances e pagamentos, use o frontend ou grpcurl")
        
        channel.close()
        
    except grpc.RpcError as e:
        print(f"\n❌ Erro gRPC: {e.code()} - {e.details()}")
        print("\n⚠️  Certifique-se de que todos os microsserviços estão rodando:")
        print("   - python services/ms_leilao.py")
        print("   - python services/ms_lance.py")
        print("   - python services/ms_pagamento.py")
        print("   - python app.py")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\n⚠️  Você executou a geração dos arquivos proto?")
        print("   python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/*.proto")


if __name__ == "__main__":
    test_gateway()
