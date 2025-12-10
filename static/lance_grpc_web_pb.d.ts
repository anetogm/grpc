import * as grpcWeb from 'grpc-web';

import * as lance_pb from './lance_pb'; // proto import: "lance.proto"


export class LanceServiceClient {
  constructor (hostname: string,
               credentials?: null | { [index: string]: string; },
               options?: null | { [index: string]: any; });

  enviarLance(
    request: lance_pb.EnviarLanceRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: lance_pb.EnviarLanceResponse) => void
  ): grpcWeb.ClientReadableStream<lance_pb.EnviarLanceResponse>;

  streamLances(
    request: lance_pb.StreamLancesRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<lance_pb.NotificacaoLance>;

  iniciarLeilao(
    request: lance_pb.IniciarLeilaoRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: lance_pb.IniciarLeilaoResponse) => void
  ): grpcWeb.ClientReadableStream<lance_pb.IniciarLeilaoResponse>;

  finalizarLeilao(
    request: lance_pb.FinalizarLeilaoRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: lance_pb.FinalizarLeilaoResponse) => void
  ): grpcWeb.ClientReadableStream<lance_pb.FinalizarLeilaoResponse>;

}

export class LanceServicePromiseClient {
  constructor (hostname: string,
               credentials?: null | { [index: string]: string; },
               options?: null | { [index: string]: any; });

  enviarLance(
    request: lance_pb.EnviarLanceRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<lance_pb.EnviarLanceResponse>;

  streamLances(
    request: lance_pb.StreamLancesRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<lance_pb.NotificacaoLance>;

  iniciarLeilao(
    request: lance_pb.IniciarLeilaoRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<lance_pb.IniciarLeilaoResponse>;

  finalizarLeilao(
    request: lance_pb.FinalizarLeilaoRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<lance_pb.FinalizarLeilaoResponse>;

}

