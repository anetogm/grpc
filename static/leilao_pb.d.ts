import * as jspb from 'google-protobuf'



export class Leilao extends jspb.Message {
  getId(): number;
  setId(value: number): Leilao;

  getNome(): string;
  setNome(value: string): Leilao;

  getDescricao(): string;
  setDescricao(value: string): Leilao;

  getValorInicial(): number;
  setValorInicial(value: number): Leilao;

  getInicio(): string;
  setInicio(value: string): Leilao;

  getFim(): string;
  setFim(value: string): Leilao;

  getStatus(): string;
  setStatus(value: string): Leilao;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Leilao.AsObject;
  static toObject(includeInstance: boolean, msg: Leilao): Leilao.AsObject;
  static serializeBinaryToWriter(message: Leilao, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Leilao;
  static deserializeBinaryFromReader(message: Leilao, reader: jspb.BinaryReader): Leilao;
}

export namespace Leilao {
  export type AsObject = {
    id: number;
    nome: string;
    descricao: string;
    valorInicial: number;
    inicio: string;
    fim: string;
    status: string;
  };
}

export class CriarLeilaoRequest extends jspb.Message {
  getNome(): string;
  setNome(value: string): CriarLeilaoRequest;

  getDescricao(): string;
  setDescricao(value: string): CriarLeilaoRequest;

  getValorInicial(): number;
  setValorInicial(value: number): CriarLeilaoRequest;

  getInicio(): string;
  setInicio(value: string): CriarLeilaoRequest;

  getFim(): string;
  setFim(value: string): CriarLeilaoRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CriarLeilaoRequest.AsObject;
  static toObject(includeInstance: boolean, msg: CriarLeilaoRequest): CriarLeilaoRequest.AsObject;
  static serializeBinaryToWriter(message: CriarLeilaoRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CriarLeilaoRequest;
  static deserializeBinaryFromReader(message: CriarLeilaoRequest, reader: jspb.BinaryReader): CriarLeilaoRequest;
}

export namespace CriarLeilaoRequest {
  export type AsObject = {
    nome: string;
    descricao: string;
    valorInicial: number;
    inicio: string;
    fim: string;
  };
}

export class CriarLeilaoResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): CriarLeilaoResponse;

  getMessage(): string;
  setMessage(value: string): CriarLeilaoResponse;

  getLeilaoId(): number;
  setLeilaoId(value: number): CriarLeilaoResponse;

  getLeilao(): Leilao | undefined;
  setLeilao(value?: Leilao): CriarLeilaoResponse;
  hasLeilao(): boolean;
  clearLeilao(): CriarLeilaoResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CriarLeilaoResponse.AsObject;
  static toObject(includeInstance: boolean, msg: CriarLeilaoResponse): CriarLeilaoResponse.AsObject;
  static serializeBinaryToWriter(message: CriarLeilaoResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CriarLeilaoResponse;
  static deserializeBinaryFromReader(message: CriarLeilaoResponse, reader: jspb.BinaryReader): CriarLeilaoResponse;
}

export namespace CriarLeilaoResponse {
  export type AsObject = {
    success: boolean;
    message: string;
    leilaoId: number;
    leilao?: Leilao.AsObject;
  };
}

export class ListarLeiloesRequest extends jspb.Message {
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListarLeiloesRequest.AsObject;
  static toObject(includeInstance: boolean, msg: ListarLeiloesRequest): ListarLeiloesRequest.AsObject;
  static serializeBinaryToWriter(message: ListarLeiloesRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListarLeiloesRequest;
  static deserializeBinaryFromReader(message: ListarLeiloesRequest, reader: jspb.BinaryReader): ListarLeiloesRequest;
}

export namespace ListarLeiloesRequest {
  export type AsObject = {
  };
}

export class ListarLeiloesResponse extends jspb.Message {
  getLeiloesList(): Array<Leilao>;
  setLeiloesList(value: Array<Leilao>): ListarLeiloesResponse;
  clearLeiloesList(): ListarLeiloesResponse;
  addLeiloes(value?: Leilao, index?: number): Leilao;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListarLeiloesResponse.AsObject;
  static toObject(includeInstance: boolean, msg: ListarLeiloesResponse): ListarLeiloesResponse.AsObject;
  static serializeBinaryToWriter(message: ListarLeiloesResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListarLeiloesResponse;
  static deserializeBinaryFromReader(message: ListarLeiloesResponse, reader: jspb.BinaryReader): ListarLeiloesResponse;
}

export namespace ListarLeiloesResponse {
  export type AsObject = {
    leiloesList: Array<Leilao.AsObject>;
  };
}

export class RegistrarInteresseRequest extends jspb.Message {
  getLeilaoId(): number;
  setLeilaoId(value: number): RegistrarInteresseRequest;

  getClienteId(): string;
  setClienteId(value: string): RegistrarInteresseRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): RegistrarInteresseRequest.AsObject;
  static toObject(includeInstance: boolean, msg: RegistrarInteresseRequest): RegistrarInteresseRequest.AsObject;
  static serializeBinaryToWriter(message: RegistrarInteresseRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): RegistrarInteresseRequest;
  static deserializeBinaryFromReader(message: RegistrarInteresseRequest, reader: jspb.BinaryReader): RegistrarInteresseRequest;
}

export namespace RegistrarInteresseRequest {
  export type AsObject = {
    leilaoId: number;
    clienteId: string;
  };
}

export class RegistrarInteresseResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): RegistrarInteresseResponse;

  getMessage(): string;
  setMessage(value: string): RegistrarInteresseResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): RegistrarInteresseResponse.AsObject;
  static toObject(includeInstance: boolean, msg: RegistrarInteresseResponse): RegistrarInteresseResponse.AsObject;
  static serializeBinaryToWriter(message: RegistrarInteresseResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): RegistrarInteresseResponse;
  static deserializeBinaryFromReader(message: RegistrarInteresseResponse, reader: jspb.BinaryReader): RegistrarInteresseResponse;
}

export namespace RegistrarInteresseResponse {
  export type AsObject = {
    success: boolean;
    message: string;
  };
}

export class CancelarInteresseRequest extends jspb.Message {
  getLeilaoId(): number;
  setLeilaoId(value: number): CancelarInteresseRequest;

  getClienteId(): string;
  setClienteId(value: string): CancelarInteresseRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CancelarInteresseRequest.AsObject;
  static toObject(includeInstance: boolean, msg: CancelarInteresseRequest): CancelarInteresseRequest.AsObject;
  static serializeBinaryToWriter(message: CancelarInteresseRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CancelarInteresseRequest;
  static deserializeBinaryFromReader(message: CancelarInteresseRequest, reader: jspb.BinaryReader): CancelarInteresseRequest;
}

export namespace CancelarInteresseRequest {
  export type AsObject = {
    leilaoId: number;
    clienteId: string;
  };
}

export class CancelarInteresseResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): CancelarInteresseResponse;

  getMessage(): string;
  setMessage(value: string): CancelarInteresseResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CancelarInteresseResponse.AsObject;
  static toObject(includeInstance: boolean, msg: CancelarInteresseResponse): CancelarInteresseResponse.AsObject;
  static serializeBinaryToWriter(message: CancelarInteresseResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CancelarInteresseResponse;
  static deserializeBinaryFromReader(message: CancelarInteresseResponse, reader: jspb.BinaryReader): CancelarInteresseResponse;
}

export namespace CancelarInteresseResponse {
  export type AsObject = {
    success: boolean;
    message: string;
  };
}

export class NotificacaoLeilao extends jspb.Message {
  getTipo(): string;
  setTipo(value: string): NotificacaoLeilao;

  getLeilaoId(): number;
  setLeilaoId(value: number): NotificacaoLeilao;

  getLeilao(): Leilao | undefined;
  setLeilao(value?: Leilao): NotificacaoLeilao;
  hasLeilao(): boolean;
  clearLeilao(): NotificacaoLeilao;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): NotificacaoLeilao.AsObject;
  static toObject(includeInstance: boolean, msg: NotificacaoLeilao): NotificacaoLeilao.AsObject;
  static serializeBinaryToWriter(message: NotificacaoLeilao, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): NotificacaoLeilao;
  static deserializeBinaryFromReader(message: NotificacaoLeilao, reader: jspb.BinaryReader): NotificacaoLeilao;
}

export namespace NotificacaoLeilao {
  export type AsObject = {
    tipo: string;
    leilaoId: number;
    leilao?: Leilao.AsObject;
  };
}

export class StreamNotificacoesRequest extends jspb.Message {
  getClienteId(): string;
  setClienteId(value: string): StreamNotificacoesRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): StreamNotificacoesRequest.AsObject;
  static toObject(includeInstance: boolean, msg: StreamNotificacoesRequest): StreamNotificacoesRequest.AsObject;
  static serializeBinaryToWriter(message: StreamNotificacoesRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): StreamNotificacoesRequest;
  static deserializeBinaryFromReader(message: StreamNotificacoesRequest, reader: jspb.BinaryReader): StreamNotificacoesRequest;
}

export namespace StreamNotificacoesRequest {
  export type AsObject = {
    clienteId: string;
  };
}

