# Script PowerShell para gerar código JavaScript gRPC-Web
# Requer: protoc e protoc-gen-grpc-web instalados

$PROTO_DIR = ".\protos"
$OUT_DIR = ".\static\generated"

# Criar diretório de saída
New-Item -ItemType Directory -Force -Path $OUT_DIR | Out-Null

# Gerar código JavaScript
& protoc -I=$PROTO_DIR `
  --js_out=import_style=commonjs:$OUT_DIR `
  --grpc-web_out=import_style=commonjs,mode=grpcwebtext:$OUT_DIR `
  $PROTO_DIR\leilao.proto `
  $PROTO_DIR\lance.proto `
  $PROTO_DIR\pagamento.proto `
  $PROTO_DIR\gateway.proto

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Código JavaScript gRPC-Web gerado em $OUT_DIR" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao gerar código JavaScript" -ForegroundColor Red
}
