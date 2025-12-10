import * as grpcWeb from 'grpc-web';

import * as leilao_pb from './leilao_pb'; // proto import: "leilao.proto"


export class LeilaoServiceClient {
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

  streamNotificacoes(
    request: leilao_pb.StreamNotificacoesRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<leilao_pb.NotificacaoLeilao>;

}

export class LeilaoServicePromiseClient {
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

  streamNotificacoes(
    request: leilao_pb.StreamNotificacoesRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<leilao_pb.NotificacaoLeilao>;

}

