import grpc
from concurrent import futures
import time
from datetime import datetime, timedelta
import threading
from flask import Flask, jsonify, request
import generated.leilao_pb2_grpc as leilao_pb2_grpc
import generated.leilao_pb2 as leilao_pb2
from generated import lance_pb2_grpc, lance_pb2


inicio = (datetime.now() + timedelta(seconds=2))
inicio_novo = inicio.isoformat()
fim = (inicio + timedelta(minutes=2)).isoformat()

leiloes = [
	{
		'id': 1,
		'nome': 'Notebook',
		'descricao': 'Macbook Pro 16" M2 Max assinado pelo Steve Jobs',
		'valor_inicial': 1000,
		'inicio': inicio_novo,
		'fim': fim,
		'status': 'ativo'
	},
	{
		'id': 2,
		'nome':'celular',
		'descricao': 'Iphone 17 Pro Max Turbo assinado pelo Steve Jobs',
		'valor_inicial': 2000,
		'inicio': inicio_novo,
        'fim': fim,
		'status': 'ativo'
	}
]

publisher_connection = None
publisher_channel = None
publisher_lock = threading.Lock()

lock = threading.Lock()

app = Flask(__name__)

class LeilaoServiceImpl(leilao_pb2_grpc.LeilaoServiceServicer):
	"""Concrete implementation of the Leilao service"""
	
	def ListarLeiloes(self, request, context):
		response = leilao_pb2.ListarLeiloesResponse()
		for leilao in leiloes:
			item = response.leiloes.add()
			item.id = leilao['id']
			item.nome = leilao['nome']
			item.descricao = leilao['descricao']
			item.valor_inicial = leilao['valor_inicial']
			item.inicio = leilao['inicio']
			item.fim = leilao['fim']
			item.status = leilao['status']
		return response
	
	def CriarLeilao(self, request, context):
		try:
			pedido = {
				'id': (len(leiloes) + 1),
				'nome':request.nome,
				'descricao': request.descricao,
				'valor_inicial': request.valor_inicial,
				'inicio': request.inicio,
				'fim': request.fim,
				'status': 'ativo'
			}
			leiloes.append(pedido)
			return leilao_pb2.CriarLeilaoResponse(success=True, leilao_id=pedido['id'])
		except Exception as e:
			print(f"Ta chegando aqui: {e}")
			return leilao_pb2.CriarLeilaoResponse(success=False, leilao_id=-1)

	def StreamNotificacoes(self, request, context):
		# stream vazio
		for _ in []:
			yield _

def publicar_evento(fila, mensagem):
	global publisher_connection, publisher_channel
	
	with publisher_lock:
		try:
			if publisher_connection is None or publisher_connection.is_closed:
				publisher_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
				publisher_channel = publisher_connection.channel()
				publisher_channel.queue_declare(queue='leilao_iniciado')
				publisher_channel.queue_declare(queue='leilao_finalizado')
			
			publisher_channel.basic_publish(exchange='', routing_key=fila, body=mensagem)
			print(f"[x] Evento publicado em {fila}: {mensagem}")
			return True
		except Exception as e:
			print(f"[ms_leilao] Error publishing event: {e}")
			publisher_connection = None
			publisher_channel = None
			return False

def converte_datetime(ativos):
	res = []
	for leilao in ativos:
		item = leilao.copy()
		for campo in ("inicio", "fim"):
			valor = item.get(campo)
			if isinstance(valor, datetime):
				item[campo] = valor.isoformat()
		res.append(item)
	return res

def gerenciar_leilao(leilao):
	channel = grpc.insecure_channel('localhost:50052')
	stub = lance_pb2_grpc.LanceServiceStub(channel)
	leilao2 = lance_pb2.LeilaoAtivo(id=leilao['id'],nome=leilao['nome'],descricao=leilao['descricao'],valor_inicial=leilao['valor_inicial'],inicio=leilao['inicio'],fim=leilao['fim'])

	inicio = leilao['inicio']
	fim = leilao['fim']

	if isinstance(inicio, str):
		inicio = datetime.fromisoformat(inicio)
	
	if isinstance(fim, str):
		fim = datetime.fromisoformat(fim)

	tempo_ate_inicio = (inicio - datetime.now()).total_seconds()
	if tempo_ate_inicio > 0:
		time.sleep(tempo_ate_inicio)
	leilao['status'] = 'ativo'
	##chamando o metodo para informar o lance que o leilao esta ativo
	print(leilao2)
	ativo = stub.IniciarLeilao(lance_pb2.IniciarLeilaoRequest(leilao=leilao2))
	print(f"Aqui está o leilao ativo: {ativo}")
	tempo_ate_fim = (fim - datetime.now()).total_seconds()
	if tempo_ate_fim > 0:
		time.sleep(tempo_ate_fim)
	leilao['status'] = 'encerrado'
	finalizado = stub.FinalizarLeilao(lance_pb2.FinalizarLeilaoRequest(leilao_id=leilao['id']))
	print(finalizado)

def main():
	threads = []
	for leilao in leiloes:
		t = threading.Thread(target=gerenciar_leilao, args=(leilao,))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()


leiloes_ativos = {}
lances_atuais = {}

def criar_request_leilao():
	request = leilao_pb2.ListarLeiloesRequest()
	return request

@app.get("/leiloes")
def get_ativos():
	channel = grpc.insecure_channel('localhost:50051')
	stub = leilao_pb2_grpc.LeilaoServiceStub(channel)
	leiloes = stub.ListarLeiloes(criar_request_leilao())
	return leiloes.json()

if __name__ == "__main__":
	def serve():
		"""Iniciar servidor gRPC"""
		server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
		leilao_pb2_grpc.add_LeilaoServiceServicer_to_server(LeilaoServiceImpl(), server)
		server.add_insecure_port('0.0.0.0:50051')
		server.start()
		print("[ms_leilao] Servidor gRPC iniciado na porta 50051")

		##Iniciar gerenciamento dos leilões existentes
		for leilao in leiloes:
			t = threading.Thread(target=gerenciar_leilao, args=(leilao,), daemon=True)
			t.start()

		try:
			server.wait_for_termination()
		except KeyboardInterrupt:
			print("[ms_leilao] Servidor encerrado")
			server.stop(0)
	threading.Thread(target=serve,daemon=True).start()
	app.run(host="127.0.0.1", port=4447, debug=False, use_reloader=False)
 
