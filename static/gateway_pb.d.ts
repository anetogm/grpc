import * as jspb from 'google-protobuf'

import * as leilao_pb from './leilao_pb'; // proto import: "leilao.proto"
import * as lance_pb from './lance_pb'; // proto import: "lance.proto"
import * as pagamento_pb from './pagamento_pb'; // proto import: "pagamento.proto"


export class NotificacaoUnificada extends jspb.Message {
  getTipo(): string;
  setTipo(value: string): NotificacaoUnificada;

  getLeilaoId(): number;
  setLeilaoId(value: number): NotificacaoUnificada;

  getUserId(): string;
  setUserId(value: string): NotificacaoUnificada;

  getValor(): number;
  setValor(value: number): NotificacaoUnificada;

  getIdVencedor(): string;
  setIdVencedor(value: string): NotificacaoUnificada;

  getLinkPagamento(): string;
  setLinkPagamento(value: string): NotificacaoUnificada;

  getStatus(): string;
  setStatus(value: string): NotificacaoUnificada;

  getMessage(): string;
  setMessage(value: string): NotificacaoUnificada;

  getLeilao(): leilao_pb.Leilao | undefined;
  setLeilao(value?: leilao_pb.Leilao): NotificacaoUnificada;
  hasLeilao(): boolean;
  clearLeilao(): NotificacaoUnificada;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): NotificacaoUnificada.AsObject;
  static toObject(includeInstance: boolean, msg: NotificacaoUnificada): NotificacaoUnificada.AsObject;
  static serializeBinaryToWriter(message: NotificacaoUnificada, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): NotificacaoUnificada;
  static deserializeBinaryFromReader(message: NotificacaoUnificada, reader: jspb.BinaryReader): NotificacaoUnificada;
}

export namespace NotificacaoUnificada {
  export type AsObject = {
    tipo: string;
    leilaoId: number;
    userId: string;
    valor: number;
    idVencedor: string;
    linkPagamento: string;
    status: string;
    message: string;
    leilao?: leilao_pb.Leilao.AsObject;
  };
}

export class StreamNotificacoesUnificadasRequest extends jspb.Message {
  getClienteId(): string;
  setClienteId(value: string): StreamNotificacoesUnificadasRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): StreamNotificacoesUnificadasRequest.AsObject;
  static toObject(includeInstance: boolean, msg: StreamNotificacoesUnificadasRequest): StreamNotificacoesUnificadasRequest.AsObject;
  static serializeBinaryToWriter(message: StreamNotificacoesUnificadasRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): StreamNotificacoesUnificadasRequest;
  static deserializeBinaryFromReader(message: StreamNotificacoesUnificadasRequest, reader: jspb.BinaryReader): StreamNotificacoesUnificadasRequest;
}

export namespace StreamNotificacoesUnificadasRequest {
  export type AsObject = {
    clienteId: string;
  };
}

