#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 3000

class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        root = os.path.dirname(__file__)
        super().__init__(*args, directory=root, **kwargs)

    def do_GET(self):
        # Map rotas amigáveis para arquivos em templates/
        if self.path == '/' or self.path == '/index.html':
            self.path = '/templates/index.html'
        elif self.path == '/cadastra_leilao':
            self.path = '/templates/cadastra_leilao.html'
        elif self.path == '/lance':
            self.path = '/templates/lance.html'
        # Qualquer /static/* já será servido do diretório raiz
        # Bloquear antigas rotas REST
        if self.path.startswith('/api/'):
            self.send_error(404, 'API REST desativada. Use gRPC-Web via Envoy.')
            return
        return super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), StaticHandler) as httpd:
        print(f"✓ Servindo arquivos estáticos em http://localhost:{PORT}")
        print("✓ Rotas: /, /cadastra_leilao, /lance e /static/*")
        print("✗ API REST desativada — use gRPC-Web pelo Envoy em :8080")
        httpd.serve_forever()
