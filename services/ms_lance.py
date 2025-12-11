from datetime import datetime
from flask import Flask ,jsonify, request
import grpc
from concurrent import futures
import json
import os
import threading

lock = threading.Lock()
app = Flask(__name__)

leiloes_ativos = {}
lances_atuais = {}

LEILAO_INATIVO = 1
LANCE_INFERIOR = 2
LANCE_VALIDADO = 3

consumer_channel = None
publisher_connection = None
publisher_channel = None
publisher_lock = threading.Lock()
import generated.lance_pb2_grpc as lance_pb2_grpc
import generated.lance_pb2 as lance_pb2

class LanceServiceImpl(lance_pb2_grpc.LanceServiceServicer):
	"""Concrete implementation of the Leilao service"""
	def EnviarLance(self, request, context):
		
		novo_lance = lance_pb2.Lance()
		novo_lance.leilao_id = request.leilao_id
		novo_lance.user_id = request.user_id
		novo_lance.valor = request.valor
		novo_lance.timestamp = (datetime.now()).isoformat()

		result = verifica_lance(novo_lance)
		try:
			if result == LANCE_VALIDADO:
				lances_atuais[novo_lance.leilao_id] = {
				'id_cliente': novo_lance.user_id,
				'valor': novo_lance.valor,
				'timestamp': novo_lance.timestamp
				}
				return lance_pb2.EnviarLanceResponse(success=1, message=f"Lance Validado no leilao {novo_lance.leilao_id}",valido=1)
			elif result == LANCE_INFERIOR:
				return lance_pb2.EnviarLanceResponse(success=0, message=f"Lance inferior que o atual no leilao {novo_lance.leilao_id}",valido=0)
		except Exception as e:
			print(f"Aqui chegou e deu esse erro {e}")
			return lance_pb2.EnviarLanceResponse(success=0, message=f"Erro ao dar lance em leilao {novo_lance.leilao_id}",valido=0)
		return lance_pb2.EnviarLanceResponse(success=0, message=f"Deu ruim geral {novo_lance.leilao_id}",valido=0)
	
	def StreamLances(self, request, context):
		return super().StreamLances(request, context)
	def IniciarLeilao(self, request, context):
        try:
            leilao = request.leilao
            leilao_id = int(leilao.id)
            with lock:
                leiloes_ativos[leilao_id] = {
                    'nome': getattr(leilao, 'nome', ''),
                    'valor': getattr(leilao, 'valor_inicial', getattr(leilao, 'valor', 0)),
                    'descricao': getattr(leilao, 'descricao', '')
                }
            print(f'[ms_lance] Leilão iniciado: {leilao_id} -> {leiloes_ativos[leilao_id]}')
            return lance_pb2.IniciarLeilaoResponse(success=1)
        except Exception as e:
            print(f'[ms_lance] Erro em IniciarLeilao: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return lance_pb2.IniciarLeilaoResponse(success=0)

    def FinalizarLeilao(self, request, context):
        try:
            leilao_id = int(request.leilao_id)
            with lock:
                vencedor = lances_atuais.pop(leilao_id, None)
                leiloes_ativos.pop(leilao_id, None)

            if vencedor:
                id_vencedor = vencedor.get('id_cliente', -1)
                valor_vencedor = vencedor.get('valor', 0)
            else:
                id_vencedor = -1
                valor_vencedor = 0

            print(f'[ms_lance] Leilão finalizado: {leilao_id}, vencedor={id_vencedor}, valor={valor_vencedor}')
            return lance_pb2.FinalizarLeilaoResponse(success=1, id_vencedor=id_vencedor, valor=valor_vencedor)
        except Exception as e:
            print(f'[ms_lance] Erro em FinalizarLeilao: {e}')
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return lance_pb2.FinalizarLeilaoResponse(success=0, id_vencedor=-1, valor=0)
	if False:
		def IniciarLeilao(self, request, context):
			try:
				leiloes_ativos[request.leilao.id] = {
					'nome': request.leilao.nome,
					'valor': request.leilao.valor_inicial,
					'descricao':request.leilao.descricao
				}
				print(f'iniciou uns leiloes {leiloes_ativos}')
				return lance_pb2.IniciarLeilaoResponse(success=1)
			except:
				return lance_pb2.IniciarLeilaoResponse(success=0)
		
		def FinalizarLeilao(self, request, context):
			id = request.leilao_id
			id_vencedor1 = lances_atuais[id]['id_cliente']
			valor_vencedor = lances_atuais[id]['valor']
			leiloes_ativos[id].pop()
			return super().FinalizarLeilaoResponse(success=1,id_vencedor=id_vencedor1,valor=valor_vencedor)


def callback_leilao_iniciado(ch, method, properties, body):
	return False

def callback_leilao_finalizado(ch, method, properties, body):
	print("Recebido em leilao_finalizado:", body)
	leilao_id = int(body.decode().split(',')[0])

	with lock:
		leiloes_ativos.pop(leilao_id, None)
		vencedor = lances_atuais.pop(leilao_id, None)

	if vencedor:
		msg_vencedor = json.dumps({'leilao_id': leilao_id, 'id_vencedor': vencedor['id_cliente'], 'valor': vencedor['valor']})
		publicar_vencedor('leilao_vencedor', msg_vencedor)
		print(f"Vencedor publicado: {msg_vencedor}")


def publish_message(routing_key, message):
	return False

def publicar_vencedor(exchange, message):
	return False                           

def verifica_lance(a: lance_pb2.Lance):
    # Check if auction exists and is active
    if a.leilao_id not in leiloes_ativos:
        return LEILAO_INATIVO
    
    # Check if this is the first bid or if it's higher than current bid
    if a.leilao_id not in lances_atuais:
        return LANCE_VALIDADO  # First bid on this auction
    
    # Check if new bid is higher than current bid
    if leiloes_ativos[a.leilao_id]['valor'] > a.valor:
        return LANCE_INFERIOR
    
    return LANCE_VALIDADO
	

@app.get("/debug/leiloes")
def debug_leiloes():
    return jsonify({
        'leiloes_ativos': list(leiloes_ativos.keys()),
        'lances_atuais': list(lances_atuais.keys())
    })

def serve():
		"""Iniciar servidor gRPC"""
		server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
		lance_pb2_grpc.add_LanceServiceServicer_to_server(LanceServiceImpl(), server)
		server.add_insecure_port('0.0.0.0:50052')
		server.start()
		print("[ms_lance] Servidor gRPC iniciado na porta 50052")

		try:
			server.wait_for_termination()
		except KeyboardInterrupt:
			print("[ms_lance] Servidor encerrado")
			server.stop(0)

if __name__ == "__main__":
	import time
	time.sleep(1)
	threading.Thread(target=serve,daemon=True).start()
	app.run(host="127.0.0.1", port=4445, debug=False, use_reloader=False)