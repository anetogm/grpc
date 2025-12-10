// Arquivo de entrada para o bundle gRPC-Web
// Importar os arquivos gerados dos .proto
import 'grpc-web';
import './gateway_pb.js';
import './gateway_grpc_web_pb.js';
import './leilao_pb.js';
import './leilao_grpc_web_pb.js';
import './lance_pb.js';
import './lance_grpc_web_pb.js';
import './pagamento_pb.js';
import './pagamento_grpc_web_pb.js';


// Expor proto globalmente para o browser (já definido pelos arquivos acima)
if (typeof window !== 'undefined') {
  window.proto = window.proto || {};
  // Os arquivos já definem proto.gateway etc. globalmente via goog.object.extend
}

// Agora importar o app.js
import './app.js';
import './cadastra.js';