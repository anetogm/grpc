import * as grpcWeb from 'grpc-web';

import * as gateway_pb from './gateway_pb'; // proto import: "gateway.proto"
import * as lance_pb from './lance_pb'; // proto import: "lance.proto"
import * as leilao_pb from './leilao_pb'; // proto import: "leilao.proto"
import * as pagamento_pb from './pagamento_pb'; // proto import: "pagamento.proto"


export class GatewayServiceClient {
  constructor (hostname: string,
               credentials?: null | { [index: string]: string; },
               options?: null | { [index: string]: any; });

  criarLeilao(
    request: leilao_pb.CriarLeilaoRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: leilao_pb.CriarLeilaoResponse) => void
  ): grpcWeb.ClientReadableStream<leilao_pb.CriarLeilaoResponse>;

  listarLeiloes(
    request: leilao_pb.ListarLeiloesRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: leilao_pb.ListarLeiloesResponse) => void
  ): grpcWeb.ClientReadableStream<leilao_pb.ListarLeiloesResponse>;

  registrarInteresse(
    request: leilao_pb.RegistrarInteresseRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: leilao_pb.RegistrarInteresseResponse) => void
  ): grpcWeb.ClientReadableStream<leilao_pb.RegistrarInteresseResponse>;

  cancelarInteresse(
    request: leilao_pb.CancelarInteresseRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: leilao_pb.CancelarInteresseResponse) => void
  ): grpcWeb.ClientReadableStream<leilao_pb.CancelarInteresseResponse>;

  enviarLance(
    request: lance_pb.EnviarLanceRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: lance_pb.EnviarLanceResponse) => void
  ): grpcWeb.ClientReadableStream<lance_pb.EnviarLanceResponse>;

  processarPagamento(
    request: pagamento_pb.ProcessarPagamentoRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: pagamento_pb.ProcessarPagamentoResponse) => void
  ): grpcWeb.ClientReadableStream<pagamento_pb.ProcessarPagamentoResponse>;

  streamNotificacoesUnificadas(
    request: gateway_pb.StreamNotificacoesUnificadasRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<gateway_pb.NotificacaoUnificada>;

}

export class GatewayServicePromiseClient {
  constructor (hostname: string,
               credentials?: null | { [index: string]: string; },
               options?: null | { [index: string]: any; });

  criarLeilao(
    request: leilao_pb.CriarLeilaoRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<leilao_pb.CriarLeilaoResponse>;

  listarLeiloes(
    request: leilao_pb.ListarLeiloesRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<leilao_pb.ListarLeiloesResponse>;

  registrarInteresse(
    request: leilao_pb.RegistrarInteresseRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<leilao_pb.RegistrarInteresseResponse>;

  cancelarInteresse(
    request: leilao_pb.CancelarInteresseRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<leilao_pb.CancelarInteresseResponse>;

  enviarLance(
    request: lance_pb.EnviarLanceRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<lance_pb.EnviarLanceResponse>;

  processarPagamento(
    request: pagamento_pb.ProcessarPagamentoRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<pagamento_pb.ProcessarPagamentoResponse>;

  streamNotificacoesUnificadas(
    request: gateway_pb.StreamNotificacoesUnificadasRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<gateway_pb.NotificacaoUnificada>;

}

