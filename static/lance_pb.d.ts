import * as jspb from 'google-protobuf'



export class Lance extends jspb.Message {
  getLeilaoId(): number;
  setLeilaoId(value: number): Lance;

  getUserId(): string;
  setUserId(value: string): Lance;

  getValor(): number;
  setValor(value: number): Lance;

  getTimestamp(): string;
  setTimestamp(value: string): Lance;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Lance.AsObject;
  static toObject(includeInstance: boolean, msg: Lance): Lance.AsObject;
  static serializeBinaryToWriter(message: Lance, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Lance;
  static deserializeBinaryFromReader(message: Lance, reader: jspb.BinaryReader): Lance;
}

export namespace Lance {
  export type AsObject = {
    leilaoId: number;
    userId: string;
    valor: number;
    timestamp: string;
  };
}

export class EnviarLanceRequest extends jspb.Message {
  getLeilaoId(): number;
  setLeilaoId(value: number): EnviarLanceRequest;

  getUserId(): string;
  setUserId(value: string): EnviarLanceRequest;

  getValor(): number;
  setValor(value: number): EnviarLanceRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): EnviarLanceRequest.AsObject;
  static toObject(includeInstance: boolean, msg: EnviarLanceRequest): EnviarLanceRequest.AsObject;
  static serializeBinaryToWriter(message: EnviarLanceRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): EnviarLanceRequest;
  static deserializeBinaryFromReader(message: EnviarLanceRequest, reader: jspb.BinaryReader): EnviarLanceRequest;
}

export namespace EnviarLanceRequest {
  export type AsObject = {
    leilaoId: number;
    userId: string;
    valor: number;
  };
}

export class EnviarLanceResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): EnviarLanceResponse;

  getMessage(): string;
  setMessage(value: string): EnviarLanceResponse;

  getValido(): boolean;
  setValido(value: boolean): EnviarLanceResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): EnviarLanceResponse.AsObject;
  static toObject(includeInstance: boolean, msg: EnviarLanceResponse): EnviarLanceResponse.AsObject;
  static serializeBinaryToWriter(message: EnviarLanceResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): EnviarLanceResponse;
  static deserializeBinaryFromReader(message: EnviarLanceResponse, reader: jspb.BinaryReader): EnviarLanceResponse;
}

export namespace EnviarLanceResponse {
  export type AsObject = {
    success: boolean;
    message: string;
    valido: boolean;
  };
}

export class NotificacaoLance extends jspb.Message {
  getTipo(): string;
  setTipo(value: string): NotificacaoLance;

  getLeilaoId(): number;
  setLeilaoId(value: number): NotificacaoLance;

  getUserId(): string;
  setUserId(value: string): NotificacaoLance;

  getValor(): number;
  setValor(value: number): NotificacaoLance;

  getIdVencedor(): string;
  setIdVencedor(value: string): NotificacaoLance;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): NotificacaoLance.AsObject;
  static toObject(includeInstance: boolean, msg: NotificacaoLance): NotificacaoLance.AsObject;
  static serializeBinaryToWriter(message: NotificacaoLance, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): NotificacaoLance;
  static deserializeBinaryFromReader(message: NotificacaoLance, reader: jspb.BinaryReader): NotificacaoLance;
}

export namespace NotificacaoLance {
  export type AsObject = {
    tipo: string;
    leilaoId: number;
    userId: string;
    valor: number;
    idVencedor: string;
  };
}

export class StreamLancesRequest extends jspb.Message {
  getClienteId(): string;
  setClienteId(value: string): StreamLancesRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): StreamLancesRequest.AsObject;
  static toObject(includeInstance: boolean, msg: StreamLancesRequest): StreamLancesRequest.AsObject;
  static serializeBinaryToWriter(message: StreamLancesRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): StreamLancesRequest;
  static deserializeBinaryFromReader(message: StreamLancesRequest, reader: jspb.BinaryReader): StreamLancesRequest;
}

export namespace StreamLancesRequest {
  export type AsObject = {
    clienteId: string;
  };
}

export class LeilaoAtivo extends jspb.Message {
  getId(): number;
  setId(value: number): LeilaoAtivo;

  getNome(): string;
  setNome(value: string): LeilaoAtivo;

  getDescricao(): string;
  setDescricao(value: string): LeilaoAtivo;

  getValorInicial(): number;
  setValorInicial(value: number): LeilaoAtivo;

  getInicio(): string;
  setInicio(value: string): LeilaoAtivo;

  getFim(): string;
  setFim(value: string): LeilaoAtivo;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): LeilaoAtivo.AsObject;
  static toObject(includeInstance: boolean, msg: LeilaoAtivo): LeilaoAtivo.AsObject;
  static serializeBinaryToWriter(message: LeilaoAtivo, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): LeilaoAtivo;
  static deserializeBinaryFromReader(message: LeilaoAtivo, reader: jspb.BinaryReader): LeilaoAtivo;
}

export namespace LeilaoAtivo {
  export type AsObject = {
    id: number;
    nome: string;
    descricao: string;
    valorInicial: number;
    inicio: string;
    fim: string;
  };
}

export class IniciarLeilaoRequest extends jspb.Message {
  getLeilao(): LeilaoAtivo | undefined;
  setLeilao(value?: LeilaoAtivo): IniciarLeilaoRequest;
  hasLeilao(): boolean;
  clearLeilao(): IniciarLeilaoRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): IniciarLeilaoRequest.AsObject;
  static toObject(includeInstance: boolean, msg: IniciarLeilaoRequest): IniciarLeilaoRequest.AsObject;
  static serializeBinaryToWriter(message: IniciarLeilaoRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): IniciarLeilaoRequest;
  static deserializeBinaryFromReader(message: IniciarLeilaoRequest, reader: jspb.BinaryReader): IniciarLeilaoRequest;
}

export namespace IniciarLeilaoRequest {
  export type AsObject = {
    leilao?: LeilaoAtivo.AsObject;
  };
}

export class IniciarLeilaoResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): IniciarLeilaoResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): IniciarLeilaoResponse.AsObject;
  static toObject(includeInstance: boolean, msg: IniciarLeilaoResponse): IniciarLeilaoResponse.AsObject;
  static serializeBinaryToWriter(message: IniciarLeilaoResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): IniciarLeilaoResponse;
  static deserializeBinaryFromReader(message: IniciarLeilaoResponse, reader: jspb.BinaryReader): IniciarLeilaoResponse;
}

export namespace IniciarLeilaoResponse {
  export type AsObject = {
    success: boolean;
  };
}

export class FinalizarLeilaoRequest extends jspb.Message {
  getLeilaoId(): number;
  setLeilaoId(value: number): FinalizarLeilaoRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): FinalizarLeilaoRequest.AsObject;
  static toObject(includeInstance: boolean, msg: FinalizarLeilaoRequest): FinalizarLeilaoRequest.AsObject;
  static serializeBinaryToWriter(message: FinalizarLeilaoRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): FinalizarLeilaoRequest;
  static deserializeBinaryFromReader(message: FinalizarLeilaoRequest, reader: jspb.BinaryReader): FinalizarLeilaoRequest;
}

export namespace FinalizarLeilaoRequest {
  export type AsObject = {
    leilaoId: number;
  };
}

export class FinalizarLeilaoResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): FinalizarLeilaoResponse;

  getIdVencedor(): string;
  setIdVencedor(value: string): FinalizarLeilaoResponse;

  getValor(): number;
  setValor(value: number): FinalizarLeilaoResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): FinalizarLeilaoResponse.AsObject;
  static toObject(includeInstance: boolean, msg: FinalizarLeilaoResponse): FinalizarLeilaoResponse.AsObject;
  static serializeBinaryToWriter(message: FinalizarLeilaoResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): FinalizarLeilaoResponse;
  static deserializeBinaryFromReader(message: FinalizarLeilaoResponse, reader: jspb.BinaryReader): FinalizarLeilaoResponse;
}

export namespace FinalizarLeilaoResponse {
  export type AsObject = {
    success: boolean;
    idVencedor: string;
    valor: number;
  };
}

