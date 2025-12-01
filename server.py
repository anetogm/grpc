#!/usr/bin/env python3
import http.server
import socketserver
import json
import grpc
import sys
import os
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Adicionar diretório generated ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

import gateway_pb2_grpc
import leilao_pb2
import lance_pb2

PORT = 3000
GATEWAY_SERVICE = 'localhost:50054'

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Rotas HTML
        if parsed_path.path == '/':
            self.serve_file('templates/index.html', 'text/html')
        elif parsed_path.path == '/cadastra_leilao':
            self.serve_file('templates/cadastra_leilao.html', 'text/html')
        elif parsed_path.path == '/lance':
            self.serve_file('templates/lance.html', 'text/html')
        elif parsed_path.path.startswith('/static/'):
            filepath = parsed_path.path[1:]  # Remove /
            if filepath.endswith('.js'):
                self.serve_file(filepath, 'application/javascript')
            else:
                self.serve_file(filepath, 'text/plain')
        # API REST
        elif parsed_path.path == '/api/leiloes':
            self.handle_listar_leiloes()
        else:
            self.send_error(404, "Página não encontrada")
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        if parsed_path.path == '/api/leiloes':
            self.handle_criar_leilao(post_data)
        elif parsed_path.path == '/api/interesse':
            self.handle_registrar_interesse(post_data)
        elif parsed_path.path == '/api/lance':
            self.handle_enviar_lance(post_data)
        else:
            self.send_error(404, "Rota não encontrada")
    
    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f"Arquivo não encontrado: {filepath}")
    
    def handle_listar_leiloes(self):
        try:
            channel = grpc.insecure_channel(GATEWAY_SERVICE)
            stub = gateway_pb2_grpc.GatewayServiceStub(channel)
            request = leilao_pb2.ListarLeiloesRequest()
            response = stub.ListarLeiloes(request)
            
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
            
            self.send_json_response({'success': True, 'leiloes': leiloes})
            channel.close()
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)}, 500)
    
    def handle_criar_leilao(self, post_data):
        try:
            data = json.loads(post_data.decode('utf-8'))
            channel = grpc.insecure_channel(GATEWAY_SERVICE)
            stub = gateway_pb2_grpc.GatewayServiceStub(channel)
            
            request = leilao_pb2.CriarLeilaoRequest(
                nome=data['nome'],
                descricao=data['descricao'],
                data_inicio=data['data_inicio'],
                data_fim=data['data_fim'],
                valor_minimo=float(data['valor_minimo'])
            )
            response = stub.CriarLeilao(request)
            
            self.send_json_response({
                'success': response.success,
                'message': response.message,
                'leilao_id': response.leilao_id
            })
            channel.close()
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)}, 500)
    
    def handle_registrar_interesse(self, post_data):
        try:
            data = json.loads(post_data.decode('utf-8'))
            channel = grpc.insecure_channel(GATEWAY_SERVICE)
            stub = gateway_pb2_grpc.GatewayServiceStub(channel)
            
            request = leilao_pb2.RegistrarInteresseRequest(
                leilao_id=int(data['leilao_id']),
                cliente_id=str(data['cliente_id'])
            )
            response = stub.RegistrarInteresse(request)
            
            self.send_json_response({
                'success': response.success,
                'message': response.message
            })
            channel.close()
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)}, 500)
    
    def handle_enviar_lance(self, post_data):
        try:
            data = json.loads(post_data.decode('utf-8'))
            channel = grpc.insecure_channel(GATEWAY_SERVICE)
            stub = gateway_pb2_grpc.GatewayServiceStub(channel)
            
            request = lance_pb2.EnviarLanceRequest(
                leilao_id=int(data['leilao_id']),
                user_id=str(data['user_id']),
                valor=float(data['valor'])
            )
            response = stub.EnviarLance(request)
            
            self.send_json_response({
                'success': response.success,
                'message': response.message,
                'valido': response.valido
            })
            channel.close()
        except Exception as e:
            self.send_json_response({'success': False, 'message': str(e)}, 500)
    
    def send_json_response(self, data, status=200):
        response = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"✓ Servidor rodando em http://localhost:{PORT}")
        print("✓ Certifique-se que o Gateway gRPC está rodando na porta 50054")
        print("\nAcesse: http://localhost:3000")
        httpd.serve_forever()
