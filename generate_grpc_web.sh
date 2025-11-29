#!/bin/bash

# Script para gerar código JavaScript gRPC-Web
# Requer: protoc e protoc-gen-grpc-web instalados

PROTO_DIR="./protos"
OUT_DIR="./static/generated"

# Criar diretório de saída
mkdir -p $OUT_DIR

# Gerar código JavaScript
protoc -I=$PROTO_DIR \
  --js_out=import_style=commonjs:$OUT_DIR \
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:$OUT_DIR \
  $PROTO_DIR/leilao.proto \
  $PROTO_DIR/lance.proto \
  $PROTO_DIR/pagamento.proto \
  $PROTO_DIR/gateway.proto

echo "✅ Código JavaScript gRPC-Web gerado em $OUT_DIR"
