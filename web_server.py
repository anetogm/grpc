from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_cors import CORS
import grpc
import sys
import os

# Adicionar diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

import gateway_pb2
import gateway_pb2_grpc
import leilao_pb2
import lance_pb2
import pagamento_pb2

app = Flask(__name__)
CORS(app)

# Cliente gRPC
GATEWAY_SERVICE = 'localhost:50054'
gateway_channel = grpc.insecure_channel(GATEWAY_SERVICE)
gateway_stub = gateway_pb2_grpc.GatewayServiceStub(gateway_channel)

# ========== ROTAS HTML ==========

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastra_leilao')
def cadastra_leilao():
    return render_template('cadastra_leilao.html')

@app.route('/lance')
def lance():
    return render_template('lance.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# ========== API REST para gRPC ==========

@app.route('/api/leiloes', methods=['GET'])
def listar_leiloes():
    try:
        request_grpc = leilao_pb2.ListarLeiloesRequest()
        response = gateway_stub.ListarLeiloes(request_grpc)
        
        leiloes = []
        for leilao in response.leiloes:
            leiloes.append({
                'id': leilao.id,
                'nome': leilao.nome,
                'descricao': leilao.descricao,
                'data_inicio': leilao.data_inicio,
                'data_fim': leilao.data_fim,
                'valor_minimo': leilao.valor_minimo,
                'status': leilao.status
            })
        
        return jsonify({'success': True, 'leiloes': leiloes})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/leiloes', methods=['POST'])
def criar_leilao():
    try:
        data = request.get_json()
        request_grpc = leilao_pb2.CriarLeilaoRequest(
            nome=data['nome'],
            descricao=data['descricao'],
            data_inicio=data['data_inicio'],
            data_fim=data['data_fim'],
            valor_minimo=float(data['valor_minimo'])
        )
        response = gateway_stub.CriarLeilao(request_grpc)
        
        return jsonify({
            'success': response.success,
            'message': response.message,
            'leilao_id': response.leilao_id
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/interesse', methods=['POST'])
def registrar_interesse():
    try:
        data = request.get_json()
        request_grpc = leilao_pb2.RegistrarInteresseRequest(
            leilao_id=int(data['leilao_id']),
            cliente_id=str(data['cliente_id'])
        )
        response = gateway_stub.RegistrarInteresse(request_grpc)
        
        return jsonify({
            'success': response.success,
            'message': response.message
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/lance', methods=['POST'])
def enviar_lance():
    try:
        data = request.get_json()
        request_grpc = lance_pb2.EnviarLanceRequest(
            leilao_id=int(data['leilao_id']),
            user_id=str(data['user_id']),
            valor=float(data['valor'])
        )
        response = gateway_stub.EnviarLance(request_grpc)
        
        return jsonify({
            'success': response.success,
            'message': response.message,
            'valido': response.valido
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("Frontend REST rodando em http://localhost:3000")
    print("Certifique-se que o Gateway gRPC está rodando na porta 50054")
    app.run(host='0.0.0.0', port=3000, debug=True)
