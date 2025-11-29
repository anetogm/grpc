// Importar bibliotecas gRPC-Web geradas
const { GatewayServiceClient } = require('./generated/gateway_grpc_web_pb');
const { ProcessarPagamentoRequest } = require('./generated/pagamento_pb');

// Cliente gRPC-Web (conecta ao Envoy Proxy)
const grpcClient = new GatewayServiceClient('http://localhost:8080', null, null);

function iniciarPagamento() {
  const leilao_id = parseInt(document.getElementById("leilao_id").value, 10);
  const cliente_id = document.getElementById("cliente_id").value;
  const valor = parseFloat(document.getElementById("valor").value);
  const moeda = document.getElementById("moeda").value || "BRL";

  const saida = document.getElementById("resultado");
  saida.textContent = "Enviando...";

  // Criar request gRPC
  const request = new ProcessarPagamentoRequest();
  request.setLeilaoId(leilao_id);
  request.setClienteId(cliente_id);
  request.setValor(valor);
  request.setMoeda(moeda);

  // Chamar método gRPC
  grpcClient.processarPagamento(request, {}, (err, response) => {
    if (err) {
      console.error("Erro:", err);
      saida.textContent = "Erro ao iniciar pagamento: " + err.message;
      return;
    }

    const resultado = {
      sucesso: response.getSucesso(),
      mensagem: response.getMensagem(),
      link_pagamento: response.getLinkPagamento(),
      transaction_id: response.getTransactionId()
    };

    saida.textContent = JSON.stringify(resultado, null, 2);

    if (resultado.link_pagamento) {
      const a = document.createElement("a");
      a.href = resultado.link_pagamento;
      a.textContent = "Abrir link de pagamento";
      a.target = "_blank";
      saida.appendChild(document.createElement("br"));
      saida.appendChild(document.createElement("br"));
      saida.appendChild(a);
    }
  });
}

window.iniciarPagamento = iniciarPagamento;