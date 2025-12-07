// Frontend agora usa gRPC-Web via Envoy
let clienteId = undefined;

// Verificar se GrpcClient está disponível
if (typeof GrpcClient === "undefined") {
  console.error(
    "GrpcClient não carregado. Verifique se grpc_client.bundle.js foi incluído."
  );
}

const client = new GrpcClient.GatewayServiceClient(
  "http://localhost:8080",
  null,
  null
);

function getUserIdFromSessionStorage() {
  let userId = sessionStorage.getItem("userId");
  if (!userId) {
    userId = "cliente_" + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem("userId", userId);
  }
  return userId;
}

function nowForDatetimeLocal() {
  const now = new Date();
  now.setSeconds(0, 0);
  const tzOffsetMin = now.getTimezoneOffset();
  const local = new Date(now.getTime() - tzOffsetMin * 60000);
  return local.toISOString().slice(0, 16);
}

async function buscaLeiloes() {
  const req = new GrpcClient.ListarLeiloesRequest();
  console.log("Buscando leilões via gRPC-Web...");
  client.listarLeiloes(req, {}, (err, resp) => {
    if (err) {
      console.error("gRPC-Web error:", err.message);
      const el = document.getElementById("demo");
      if (el) el.textContent = "Erro: " + err.message;
      return;
    }
    const leiloesList = resp.getLeiloesList();
    const leiloes = leiloesList.map((l) => ({
      id: l.getId(),
      nome: l.getNome(),
      descricao: l.getDescricao(),
      inicio: l.getInicio(),
      fim: l.getFim(),
      valor_inicial: l.getValorInicial(),
      status: l.getStatus(),
    }));
    renderLeiloes(leiloes);
  });
}

async function registrarInteresse(leilaoId) {
  try {
    if (!clienteId) clienteId = getUserIdFromSessionStorage();
    const req = new GrpcClient.RegistrarInteresseRequest();
    req.setLeilaoId(leilaoId);
    req.setClienteId(clienteId);
    client.registrarInteresse(req, {}, (err, resp) => {
      if (err) {
        console.error("Erro ao registrar interesse:", err.message);
        alert("Erro ao registrar interesse: " + err.message);
        return;
      }
      alert(resp.getMessage() || "Interesse registrado");
      if (resp.getSuccess()) buscaLeiloes();
    });
  } catch (error) {
    console.error("Erro ao registrar interesse:", error);
    alert("Erro ao registrar interesse: " + error.message);
  }
}

function renderLeiloes(leiloes) {
  const container = document.getElementById("demo");

  if (leiloes.length === 0) {
    container.innerHTML = "<p>Nenhum leilão encontrado</p>";
    return;
  }

  let html = '<div style="display: grid; gap: 20px;">';

  leiloes.forEach((leilao) => {
    const statusClass = leilao.status === "ativo" ? "ativo" : "inativo";
    html += `
            <div style="border: 1px solid #ccc; padding: 15px; border-radius: 8px;">
                <h3>${leilao.nome}</h3>
                <p>${leilao.descricao}</p>
                <p><strong>Status:</strong> <span class="${statusClass}">${
      leilao.status
    }</span></p>
                <p><strong>Valor Inicial:</strong> R$ ${leilao.valor_inicial.toFixed(
                  2
                )}</p>
                <p><strong>Início:</strong> ${new Date(
                  leilao.inicio
                ).toLocaleString("pt-BR")}</p>
                <p><strong>Fim:</strong> ${new Date(leilao.fim).toLocaleString(
                  "pt-BR"
                )}</p>
                ${
                  leilao.status === "ativo"
                    ? `<button onclick="registrarInteresse(${leilao.id})">Registrar Interesse</button>`
                    : ""
                }
            </div>
        `;
  });

  html += "</div>";
  container.innerHTML = html;
}

// Auto-carregar leilões ao abrir a página
if (document.getElementById("demo")) {
  window.addEventListener("DOMContentLoaded", () => {
    buscaLeiloes();
  });
}
