// Importar bibliotecas gRPC-Web geradas
const { GatewayServiceClient } = require('./generated/gateway_grpc_web_pb');
const { 
  ListarLeiloesRequest, 
  RegistrarInteresseRequest, 
  CancelarInteresseRequest,
  StreamNotificacoesUnificadasRequest 
} = require('./generated/gateway_pb');

// Cliente gRPC-Web (conecta ao Envoy Proxy)
const grpcClient = new GatewayServiceClient('http://localhost:8080', null, null);
let clienteId = getUserIdFromSessionStorage();
let notificationStream = null;

function nowForDatetimeLocal() {
  const now = new Date();
  now.setSeconds(0, 0);
  const tzOffsetMin = now.getTimezoneOffset();
  const local = new Date(now.getTime() - tzOffsetMin * 60000);
  return local.toISOString().slice(0, 16);
}

function buscaLeiloes() {
  const request = new ListarLeiloesRequest();
  
  grpcClient.listarLeiloes(request, {}, (err, response) => {
    if (err) {
      console.error("Erro ao buscar leilões:", err);
      document.getElementById("demo").textContent = "Erro ao buscar leilões: " + err.message;
      return;
    }
    
    const leiloes = response.getLeiloesList().map(leilao => ({
      id: leilao.getId(),
      nome: leilao.getNome(),
      descricao: leilao.getDescricao(),
      data_inicio: leilao.getDataInicio(),
      data_fim: leilao.getDataFim(),
      valor_minimo: leilao.getValorMinimo(),
      status: leilao.getStatus()
    }));
    
    renderLeiloes(leiloes);
  });
}

function registrarInteresse(leilaoId) {
  console.log("Tentando registrar interesse:", leilaoId, clienteId);
  
  const request = new RegistrarInteresseRequest();
  request.setLeilaoId(leilaoId);
  request.setClienteId(clienteId);
  
  grpcClient.registrarInteresse(request, {}, (err, response) => {
    if (err) {
      console.error("Erro:", err);
      alert("Erro ao registrar interesse: " + err.message);
      return;
    }
    
    alert(response.getMessage());
  });
}

function cancelarInteresse(leilaoId) {
  const request = new CancelarInteresseRequest();
  request.setLeilaoId(leilaoId);
  request.setClienteId(clienteId);
  
  grpcClient.cancelarInteresse(request, {}, (err, response) => {
    if (err) {
      console.error("Erro:", err);
      alert("Erro ao cancelar interesse: " + err.message);
      return;
    }
    
    alert(response.getMessage());
  });
}

function renderLeiloes(lista) {
  const demoEl = document.getElementById("demo");
  demoEl.innerHTML = "";

  if (lista.length === 0) {
    demoEl.textContent = "Nenhum leilão ativo";
    return;
  }

  lista.forEach((l) => {
    const div = document.createElement("div");
    div.style.marginBottom = "10px";
    div.textContent = `${l.id} - ${l.nome || ""} (${l.descricao || ""})`;

    const btnRegistrar = document.createElement("button");
    btnRegistrar.textContent = "Registrar Interesse";
    btnRegistrar.style.marginLeft = "10px";
    btnRegistrar.onclick = () => registrarInteresse(l.id);

    const btnCancelar = document.createElement("button");
    btnCancelar.textContent = "Cancelar Interesse";
    btnCancelar.style.marginLeft = "5px";
    btnCancelar.onclick = () => cancelarInteresse(l.id);

    div.appendChild(btnRegistrar);
    div.appendChild(btnCancelar);

    demoEl.appendChild(div);
  });
}

function conectarStreamGrpc() {
  const request = new StreamNotificacoesUnificadasRequest();
  request.setClienteId(clienteId);
  
  // Criar stream de notificações
  notificationStream = grpcClient.streamNotificacoesUnificadas(request, {});
  
  notificationStream.on('data', (notificacao) => {
    console.log("Notificação gRPC:", notificacao.toObject());
    
    const tipo = notificacao.getTipo();
    const dados = notificacao.getDados();
    
    try {
      const data = JSON.parse(dados);
      
      if (tipo === "novo_lance_valido") {
        alert(`Novo lance válido no leilão ${data.leilao_id}: R$ ${data.valor}`);
        buscaLeiloes();
      } else if (tipo === "lance_invalido") {
        alert("Seu lance foi inválido.");
      } else if (tipo === "vencedor_leilao") {
        alert(`Leilão ${data.leilao_id} encerrado. Vencedor: ${data.id_vencedor}`);
      } else if (tipo === "link_pagamento") {
        exibirLinkPagamento(data.link_pagamento);
      } else if (tipo === "status_pagamento") {
        alert(`Status do pagamento: ${data.status}`);
      }
    } catch (e) {
      console.error("Erro ao processar notificação:", e);
    }
  });
  
  notificationStream.on('error', (err) => {
    console.error("Erro no stream gRPC:", err);
    // Tentar reconectar após 5 segundos
    setTimeout(() => {
      console.log("Tentando reconectar stream...");
      conectarStreamGrpc();
    }, 5000);
  });
  
  notificationStream.on('end', () => {
    console.log("Stream gRPC finalizado.");
    // Reconectar automaticamente
    setTimeout(() => conectarStreamGrpc(), 1000);
  });
  
  console.log("Stream gRPC conectado.");
}

function getUserIdFromSessionStorage() {
  let userId = sessionStorage.getItem("userId");
  if (!userId) {
    userId = crypto.randomUUID();
    sessionStorage.setItem("userId", userId);
  }
  return userId;
}

function exibirLinkPagamento(link) {
  const demoEl = document.getElementById("demo");
  const linkDiv = document.createElement("div");
  linkDiv.style.marginTop = "20px";
  linkDiv.style.padding = "10px";
  linkDiv.style.border = "1px solid #ccc";
  linkDiv.style.backgroundColor = "#f9f9f9";
  linkDiv.innerHTML = `<strong>Link de Pagamento:</strong> <a href="${link}" target="_blank">${link}</a>`;
  demoEl.appendChild(linkDiv);
}

window.onload = function () {
  conectarStreamGrpc();
  buscaLeiloes();
};
