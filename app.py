from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS
from flask_sse import sse
import grpc
from google.protobuf.json_format import MessageToDict
from flask import jsonify
import requests
import secrets
import threading
import json
import time
import redis
from services.generated import leilao_pb2_grpc, leilao_pb2
from services.generated import lance_pb2_grpc, lance_pb2

# TODO refazer a logica do sse agora que tamo usando grpc no lugar do rabbitmq

lock = threading.Lock()
rabbitmq_lock = threading.Lock()
channel = None
app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/0"
app.register_blueprint(sse, url_prefix='/stream')

app.secret_key = secrets.token_hex(16)
CORS(app)

leiloes = []
redis_client = redis.from_url(app.config["REDIS_URL"])

url_mslance = 'http://localhost:4445'
url_msleilao = 'http://localhost:4447'

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/pagamento")
def pagamento_page():
    return render_template("pagar.html")

@app.get("/leiloes")
def get_leiloes():
    channel = grpc.insecure_channel('localhost:50051')
    stub = leilao_pb2_grpc.LeilaoServiceStub(channel)
    leiloes = stub.ListarLeiloes(leilao_pb2.ListarLeiloesRequest())
    resposta_dict = MessageToDict(leiloes, preserving_proto_field_name=True)
    print(jsonify(resposta_dict))
    return jsonify(resposta_dict)

@app.get("/cadastra_leilao")
def cadastra_leilao_page():
    return render_template("cadastra_leilao.html")

@app.get("/lance")
def lance_page():
    return render_template("lance.html")

@app.post("/cadastra_leilao")
def cadastra_leilao():
        item = (request.form.get('item') or '').strip()
        descricao = request.form.get('descricao', '')
        valor_inicial = request.form.get('valor_inicial', 0)
        inicio = request.form.get('inicio', '')
        fim = request.form.get('fim', '')

        if not item:
            return jsonify({'error': 'item é obrigatório'}), 400

        novo = {'item': item, 'descricao': descricao, 'valor_inicial': valor_inicial, 'inicio': inicio, 'fim': fim}

        channel = grpc.insecure_channel('localhost:50051')
        stub = leilao_pb2_grpc.LeilaoServiceStub(channel)

        novo_leilao = leilao_pb2.CriarLeilaoRequest()
        novo_leilao.nome = novo['item']
        novo_leilao.descricao = novo['descricao']
        novo_leilao.valor_inicial = int(novo['valor_inicial'])
        novo_leilao.inicio = novo['inicio']
        novo_leilao.fim = novo['fim']

        leiloes = stub.CriarLeilao(novo_leilao)
        resposta_dict = MessageToDict(leiloes, preserving_proto_field_name=True)
        print(resposta_dict)
        return redirect("/cadastra_leilao?success=1")

@app.post("/lance")
def lance():
    data = request.get_json()
    leilao_id = data.get("leilao_id")
    user_id = data.get("user_id")
    valor = data.get("valor")

    if not leilao_id or not user_id or not valor:
        return jsonify({"error": "Dados incompletos"}), 400

    channel = grpc.insecure_channel('localhost:50052')
    stub = lance_pb2_grpc.LanceServiceStub(channel)
    
    novo_lance = lance_pb2.EnviarLanceRequest()
    novo_lance.user_id = user_id
    novo_lance.leilao_id = int(leilao_id)
    novo_lance.valor = valor

    resultado = stub.EnviarLance(novo_lance)
    resultado_dic = MessageToDict(resultado, preserving_proto_field_name=True)
    print(f"DEBUG - resultado do lance: {resultado_dic}")
    
    # CORREÇÃO: verificar 'success' ao invés de 'sucesso'
    if resultado_dic.get('success', False):  
        interessados = redis_client.smembers(f'interesses:{leilao_id}')
        print(f"Interessados no leilão {leilao_id}: {list(interessados)}")
        for cliente_id in interessados:
            channel_name = cliente_id.decode('utf-8')
            message = {
                "tipo": "lance",
                "message": "Novo lance no leilão",
                "leilao_id": leilao_id,
                "valor": valor,
                "user_id": user_id
            }
            print(f"Publicando SSE para channel '{channel_name}': {message}")
            sse.publish(message, type='lance', channel=channel_name) 
    
    return jsonify(resultado_dic)

@app.post("/registrar_interesse")
def registrar_interesse():
    data = request.get_json()
    leilao_id = data.get('leilao_id')
    cliente_id = data.get('cliente_id')
    print(f"Registrando interesse: leilao_id={leilao_id}, cliente_id={cliente_id}")
    if not leilao_id or not cliente_id:
        return jsonify({'error': 'leilao_id e cliente_id são obrigatórios'}), 400
    
    with lock:
        redis_client.sadd(f'interesses:{leilao_id}', cliente_id)
    
    return jsonify({'message': 'Interesse registrado com sucesso'})

@app.post("/cancelar_interesse")
def cancelar_interesse():
    data = request.get_json()
    leilao_id = data.get('leilao_id')
    cliente_id = data.get('cliente_id')
    
    if not leilao_id or not cliente_id:
        return jsonify({'error': 'leilao_id e cliente_id são obrigatórios'}), 400
    
    with lock:
        redis_client.srem(f'interesses:{leilao_id}', cliente_id)

        if redis_client.scard(f'interesses:{leilao_id}') == 0:
            redis_client.delete(f'interesses:{leilao_id}')
    
    return jsonify({'message': 'Interesse cancelado com sucesso'})

@app.post("/notificar_vencedor")
def notificar_vencedor():
    data = request.get_json()
    leilao_id = data.get('leilao_id')
    id_vencedor = data.get('id_vencedor')
    valor = data.get('valor')
    
    print(f"Recebido vencedor do leilão {leilao_id}: {id_vencedor} com valor {valor}")
    
    # ve quem ta interessado no leilao
    interessados = redis_client.smembers(f'interesses:{leilao_id}')
    
    for cliente_id in interessados:
        channel_name = cliente_id.decode('utf-8')
        
        # verifica se o cliente é o vencedor
        if cliente_id.decode('utf-8') == id_vencedor and id_vencedor != '-1':
            message = {
                "tipo": "vencedor_leilao",
                "leilao_id": leilao_id,
                "id_vencedor": id_vencedor,
                "valor": valor,
                "venceu": True,
                "message": f"Parabéns! Você venceu o leilão {leilao_id} com o lance de R$ {valor}"
            }
        else:
            print("mnesagem pro perdedor")
            message = {
                "tipo": "vencedor_leilao",
                "leilao_id": leilao_id,
                "id_vencedor": id_vencedor,
                "valor": valor,
                "venceu": False,
                "message": f"Leilão {leilao_id} encerrado. Vencedor: {id_vencedor if id_vencedor != '-1' else 'Sem vencedor'}"
            }
        
        print(f"Publicando SSE para channel '{channel_name}': {message}")
        sse.publish(message, type='vencedor', channel=channel_name)
    
    redis_client.delete(f'interesses:{leilao_id}')
    
    return jsonify({'message': 'Vencedor notificado com sucesso'})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4444, debug=False, use_reloader=False)