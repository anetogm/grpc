import * as grpcWeb from 'grpc-web';

import * as pagamento_pb from './pagamento_pb'; // proto import: "pagamento.proto"


export class PagamentoServiceClient {
  constructor (hostname: string,
               credentials?: null | { [index: string]: string; },
               options?: null | { [index: string]: any; });

  processarPagamento(
    request: pagamento_pb.ProcessarPagamentoRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: pagamento_pb.ProcessarPagamentoResponse) => void
  ): grpcWeb.ClientReadableStream<pagamento_pb.ProcessarPagamentoResponse>;

  streamPagamentos(
    request: pagamento_pb.StreamPagamentosRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<pagamento_pb.NotificacaoPagamento>;

  notificarVencedor(
    request: pagamento_pb.NotificarVencedorRequest,
    metadata: grpcWeb.Metadata | undefined,
    callback: (err: grpcWeb.RpcError,
               response: pagamento_pb.NotificarVencedorResponse) => void
  ): grpcWeb.ClientReadableStream<pagamento_pb.NotificarVencedorResponse>;

}

export class PagamentoServicePromiseClient {
  constructor (hostname: string,
               credentials?: null | { [index: string]: string; },
               options?: null | { [index: string]: any; });

  processarPagamento(
    request: pagamento_pb.ProcessarPagamentoRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<pagamento_pb.ProcessarPagamentoResponse>;

  streamPagamentos(
    request: pagamento_pb.StreamPagamentosRequest,
    metadata?: grpcWeb.Metadata
  ): grpcWeb.ClientReadableStream<pagamento_pb.NotificacaoPagamento>;

  notificarVencedor(
    request: pagamento_pb.NotificarVencedorRequest,
    metadata?: grpcWeb.Metadata
  ): Promise<pagamento_pb.NotificarVencedorResponse>;

}

