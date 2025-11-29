"""
Exemplos de Uso dos Serviços gRPC
Execute após gerar os arquivos proto e iniciar os microsserviços
"""

import grpc
import sys
import os
from datetime import datetime, timedelta

# Adicionar diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

import gateway_pb2
import gateway_pb2_grpc
import leilao_pb2
import lance_pb2
import pagamento_pb2


def exemplo_basico():
    """Exemplo básico: Listar leilões"""
    print("\n=== Exemplo 1: Listar Leilões ===\n")
    
    channel = grpc.insecure_channel('localhost:50054')
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    
    response = stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
    
    for leilao in response.leiloes:
        print(f"📦 Leilão #{leilao.id}")
        print(f"   Nome: {leilao.nome}")
        print(f"   Valor inicial: R$ {leilao.valor_inicial}")
        print(f"   Status: {leilao.status}")
        print()
    
    channel.close()


def exemplo_criar_leilao():
    """Exemplo: Criar novo leilão"""
    print("\n=== Exemplo 2: Criar Novo Leilão ===\n")
    
    channel = grpc.insecure_channel('localhost:50054')
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    
    inicio = (datetime.now() + timedelta(seconds=10)).isoformat()
    fim = (datetime.now() + timedelta(minutes=5)).isoformat()
    
    request = leilao_pb2.CriarLeilaoRequest(
        nome="PlayStation 5",
        descricao="PS5 com 2 controles e 3 jogos",
        valor_inicial=2000.0,
        inicio=inicio,
        fim=fim
    )
    
    response = stub.CriarLeilao(request)
    
    if response.success:
        print(f"✅ Leilão criado com sucesso!")
        print(f"   ID: {response.leilao_id}")
        print(f"   Nome: {response.leilao.nome}")
        print(f"   Início: {response.leilao.inicio}")
    else:
        print(f"❌ Erro: {response.message}")
    
    channel.close()


def exemplo_registrar_interesse():
    """Exemplo: Registrar interesse em leilão"""
    print("\n=== Exemplo 3: Registrar Interesse ===\n")
    
    channel = grpc.insecure_channel('localhost:50054')
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    
    request = leilao_pb2.RegistrarInteresseRequest(
        leilao_id=1,
        cliente_id="user_789"
    )
    
    response = stub.RegistrarInteresse(request)
    
    if response.success:
        print(f"✅ {response.message}")
    else:
        print(f"❌ Erro: {response.message}")
    
    channel.close()


def exemplo_enviar_lance():
    """Exemplo: Enviar lance"""
    print("\n=== Exemplo 4: Enviar Lance ===\n")
    
    channel = grpc.insecure_channel('localhost:50054')
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    
    request = lance_pb2.EnviarLanceRequest(
        leilao_id=1,
        user_id="user_789",
        valor=1100.0
    )
    
    response = stub.EnviarLance(request)
    
    if response.success and response.valido:
        print(f"✅ Lance aceito!")
        print(f"   Valor: R$ {request.valor}")
    else:
        print(f"❌ Lance recusado: {response.message}")
    
    channel.close()


def exemplo_stream_notificacoes():
    """Exemplo: Receber notificações em tempo real"""
    print("\n=== Exemplo 5: Stream de Notificações (10 segundos) ===\n")
    print("Aguardando notificações...\n")
    
    channel = grpc.insecure_channel('localhost:50054')
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    
    request = gateway_pb2.StreamNotificacoesUnificadasRequest(
        cliente_id="user_789"
    )
    
    import signal
    import sys
    
    # Configurar timeout
    def timeout_handler(signum, frame):
        raise TimeoutError()
    
    try:
        # Windows não tem signal.alarm, usar threading
        import threading
        import time
        
        stop_event = threading.Event()
        
        def timeout():
            time.sleep(10)
            stop_event.set()
        
        timeout_thread = threading.Thread(target=timeout, daemon=True)
        timeout_thread.start()
        
        for notificacao in stub.StreamNotificacoesUnificadas(request):
            if stop_event.is_set():
                break
                
            print(f"📩 Notificação recebida:")
            print(f"   Tipo: {notificacao.tipo}")
            print(f"   Leilão: {notificacao.leilao_id}")
            
            if notificacao.tipo == "novo_lance_valido":
                print(f"   Valor: R$ {notificacao.valor}")
                print(f"   Cliente: {notificacao.user_id}")
            elif notificacao.tipo == "vencedor_leilao":
                print(f"   Vencedor: {notificacao.id_vencedor}")
                print(f"   Valor final: R$ {notificacao.valor}")
            elif notificacao.tipo == "link_pagamento":
                print(f"   Link: {notificacao.link_pagamento}")
            
            print()
        
        print("✅ Stream finalizado")
        
    except KeyboardInterrupt:
        print("\n⚠️  Stream interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        channel.close()


def exemplo_fluxo_completo():
    """Exemplo: Fluxo completo de leilão"""
    print("\n=== Exemplo 6: Fluxo Completo ===\n")
    
    channel = grpc.insecure_channel('localhost:50054')
    stub = gateway_pb2_grpc.GatewayServiceStub(channel)
    
    print("1️⃣ Listando leilões disponíveis...")
    response = stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
    print(f"   Encontrados {len(response.leiloes)} leilões\n")
    
    if len(response.leiloes) > 0:
        leilao_id = response.leiloes[0].id
        cliente_id = "user_complete_flow"
        
        print(f"2️⃣ Registrando interesse no leilão #{leilao_id}...")
        response = stub.RegistrarInteresse(leilao_pb2.RegistrarInteresseRequest(
            leilao_id=leilao_id,
            cliente_id=cliente_id
        ))
        print(f"   {response.message}\n")
        
        print(f"3️⃣ Enviando lance de R$ 1500...")
        response = stub.EnviarLance(lance_pb2.EnviarLanceRequest(
            leilao_id=leilao_id,
            user_id=cliente_id,
            valor=1500.0
        ))
        if response.valido:
            print(f"   ✅ Lance aceito!\n")
        else:
            print(f"   ❌ {response.message}\n")
        
        print(f"4️⃣ Enviando lance maior de R$ 1600...")
        response = stub.EnviarLance(lance_pb2.EnviarLanceRequest(
            leilao_id=leilao_id,
            user_id=cliente_id,
            valor=1600.0
        ))
        if response.valido:
            print(f"   ✅ Lance aceito!\n")
        else:
            print(f"   ❌ {response.message}\n")
        
        print(f"5️⃣ Cancelando interesse...")
        response = stub.CancelarInteresse(leilao_pb2.CancelarInteresseRequest(
            leilao_id=leilao_id,
            cliente_id=cliente_id
        ))
        print(f"   {response.message}\n")
    
    channel.close()
    print("✅ Fluxo completo executado!")


def menu():
    """Menu interativo"""
    while True:
        print("\n" + "="*60)
        print("🎯 EXEMPLOS DE USO - Sistema de Leilões gRPC")
        print("="*60)
        print("\n1. Listar leilões")
        print("2. Criar novo leilão")
        print("3. Registrar interesse")
        print("4. Enviar lance")
        print("5. Stream de notificações (10s)")
        print("6. Fluxo completo")
        print("0. Sair")
        print()
        
        escolha = input("Escolha uma opção: ").strip()
        
        try:
            if escolha == "1":
                exemplo_basico()
            elif escolha == "2":
                exemplo_criar_leilao()
            elif escolha == "3":
                exemplo_registrar_interesse()
            elif escolha == "4":
                exemplo_enviar_lance()
            elif escolha == "5":
                exemplo_stream_notificacoes()
            elif escolha == "6":
                exemplo_fluxo_completo()
            elif escolha == "0":
                print("\n👋 Até logo!")
                break
            else:
                print("\n❌ Opção inválida!")
        except grpc.RpcError as e:
            print(f"\n❌ Erro gRPC: {e.code()} - {e.details()}")
            print("⚠️  Certifique-se de que os microsserviços estão rodando!")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    print("\n🚀 Sistema de Leilões gRPC - Exemplos de Uso")
    print("="*60)
    
    try:
        # Testar conexão
        channel = grpc.insecure_channel('localhost:50054')
        stub = gateway_pb2_grpc.GatewayServiceStub(channel)
        stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest(), timeout=2)
        channel.close()
        
        print("\n✅ Conexão estabelecida com o Gateway!")
        print("📡 Pronto para executar os exemplos")
        
        menu()
        
    except grpc.RpcError as e:
        print("\n❌ Não foi possível conectar ao Gateway gRPC")
        print("\n⚠️  Certifique-se de que os microsserviços estão rodando:")
        print("   1. python services/ms_leilao.py")
        print("   2. python services/ms_lance.py")
        print("   3. python services/ms_pagamento.py")
        print("   4. python app.py")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\n⚠️  Você executou a geração dos arquivos proto?")
        print("   python -m grpc_tools.protoc -I./protos --python_out=./generated --grpc_python_out=./generated ./protos/*.proto")
