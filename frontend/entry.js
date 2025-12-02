// Entry bundler para gRPC-Web (esbuild IIFE -> window.GrpcClient)
// Requer arquivos gerados por protoc em ./web_generated
const gw = require("../web_generated/gateway_grpc_web_pb");
const leilao = require("../web_generated/leilao_pb");
const lance = require("../web_generated/lance_pb");
const pagamento = require("../web_generated/pagamento_pb");

// Exporte classes necessárias para o navegador
export const GatewayServiceClient =
  gw.GatewayServiceClient ||
  (gw.proto && gw.proto.gateway && gw.proto.gateway.GatewayServiceClient);

export const ListarLeiloesRequest =
  leilao.ListarLeiloesRequest ||
  (leilao.proto &&
    leilao.proto.leilao &&
    leilao.proto.leilao.ListarLeiloesRequest);
export const CriarLeilaoRequest =
  leilao.CriarLeilaoRequest ||
  (leilao.proto &&
    leilao.proto.leilao &&
    leilao.proto.leilao.CriarLeilaoRequest);
export const RegistrarInteresseRequest =
  leilao.RegistrarInteresseRequest ||
  (leilao.proto &&
    leilao.proto.leilao &&
    leilao.proto.leilao.RegistrarInteresseRequest);

export const EnviarLanceRequest =
  lance.EnviarLanceRequest ||
  (lance.proto && lance.proto.lance && lance.proto.lance.EnviarLanceRequest);
