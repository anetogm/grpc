import * as jspb from 'google-protobuf'



export class ProcessarPagamentoRequest extends jspb.Message {
  getLeilaoId(): number;
  setLeilaoId(value: number): ProcessarPagamentoRequest;

  getClienteId(): string;
  setClienteId(value: string): ProcessarPagamentoRequest;

  getValor(): number;
  setValor(value: number): ProcessarPagamentoRequest;

  getMoeda(): string;
  setMoeda(value: string): ProcessarPagamentoRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ProcessarPagamentoRequest.AsObject;
  static toObject(includeInstance: boolean, msg: ProcessarPagamentoRequest): ProcessarPagamentoRequest.AsObject;
  static serializeBinaryToWriter(message: ProcessarPagamentoRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ProcessarPagamentoRequest;
  static deserializeBinaryFromReader(message: ProcessarPagamentoRequest, reader: jspb.BinaryReader): ProcessarPagamentoRequest;
}

export namespace ProcessarPagamentoRequest {
  export type AsObject = {
    leilaoId: number;
    clienteId: string;
    valor: number;
    moeda: string;
  };
}

export class ProcessarPagamentoResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): ProcessarPagamentoResponse;

  getMessage(): string;
  setMessage(value: string): ProcessarPagamentoResponse;

  getIdTransacao(): string;
  setIdTransacao(value: string): ProcessarPagamentoResponse;

  getLinkPagamento(): string;
  setLinkPagamento(value: string): ProcessarPagamentoResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ProcessarPagamentoResponse.AsObject;
  static toObject(includeInstance: boolean, msg: ProcessarPagamentoResponse): ProcessarPagamentoResponse.AsObject;
  static serializeBinaryToWriter(message: ProcessarPagamentoResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ProcessarPagamentoResponse;
  static deserializeBinaryFromReader(message: ProcessarPagamentoResponse, reader: jspb.BinaryReader): ProcessarPagamentoResponse;
}

export namespace ProcessarPagamentoResponse {
  export type AsObject = {
    success: boolean;
    message: string;
    idTransacao: string;
    linkPagamento: string;
  };
}

export class NotificacaoPagamento extends jspb.Message {
  getTipo(): string;
  setTipo(value: string): NotificacaoPagamento;

  getLeilaoId(): number;
  setLeilaoId(value: number): NotificacaoPagamento;

  getClienteId(): string;
  setClienteId(value: string): NotificacaoPagamento;

  getIdTransacao(): string;
  setIdTransacao(value: string): NotificacaoPagamento;

  getLinkPagamento(): string;
  setLinkPagamento(value: string): NotificacaoPagamento;

  getStatus(): string;
  setStatus(value: string): NotificacaoPagamento;

  getValor(): number;
  setValor(value: number): NotificacaoPagamento;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): NotificacaoPagamento.AsObject;
  static toObject(includeInstance: boolean, msg: NotificacaoPagamento): NotificacaoPagamento.AsObject;
  static serializeBinaryToWriter(message: NotificacaoPagamento, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): NotificacaoPagamento;
  static deserializeBinaryFromReader(message: NotificacaoPagamento, reader: jspb.BinaryReader): NotificacaoPagamento;
}

export namespace NotificacaoPagamento {
  export type AsObject = {
    tipo: string;
    leilaoId: number;
    clienteId: string;
    idTransacao: string;
    linkPagamento: string;
    status: string;
    valor: number;
  };
}

export class StreamPagamentosRequest extends jspb.Message {
  getClienteId(): string;
  setClienteId(value: string): StreamPagamentosRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): StreamPagamentosRequest.AsObject;
  static toObject(includeInstance: boolean, msg: StreamPagamentosRequest): StreamPagamentosRequest.AsObject;
  static serializeBinaryToWriter(message: StreamPagamentosRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): StreamPagamentosRequest;
  static deserializeBinaryFromReader(message: StreamPagamentosRequest, reader: jspb.BinaryReader): StreamPagamentosRequest;
}

export namespace StreamPagamentosRequest {
  export type AsObject = {
    clienteId: string;
  };
}

export class NotificarVencedorRequest extends jspb.Message {
  getLeilaoId(): number;
  setLeilaoId(value: number): NotificarVencedorRequest;

  getIdVencedor(): string;
  setIdVencedor(value: string): NotificarVencedorRequest;

  getValor(): number;
  setValor(value: number): NotificarVencedorRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): NotificarVencedorRequest.AsObject;
  static toObject(includeInstance: boolean, msg: NotificarVencedorRequest): NotificarVencedorRequest.AsObject;
  static serializeBinaryToWriter(message: NotificarVencedorRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): NotificarVencedorRequest;
  static deserializeBinaryFromReader(message: NotificarVencedorRequest, reader: jspb.BinaryReader): NotificarVencedorRequest;
}

export namespace NotificarVencedorRequest {
  export type AsObject = {
    leilaoId: number;
    idVencedor: string;
    valor: number;
  };
}

export class NotificarVencedorResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): NotificarVencedorResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): NotificarVencedorResponse.AsObject;
  static toObject(includeInstance: boolean, msg: NotificarVencedorResponse): NotificarVencedorResponse.AsObject;
  static serializeBinaryToWriter(message: NotificarVencedorResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): NotificarVencedorResponse;
  static deserializeBinaryFromReader(message: NotificarVencedorResponse, reader: jspb.BinaryReader): NotificarVencedorResponse;
}

export namespace NotificarVencedorResponse {
  export type AsObject = {
    success: boolean;
  };
}

