// Cliente REST simples (substitui gRPC-Web)
const API_URL = "http://localhost:3000/api";
let clienteId = getUserIdFromSessionStorage();

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
  try {
    const response = await fetch(`${API_URL}/leiloes`);
    const data = await response.json();

    if (data.success) {
      renderLeiloes(data.leiloes);
    } else {
      document.getElementById("demo").textContent = "Erro: " + data.message;
    }
  } catch (error) {
    console.error("Erro ao buscar leilões:", error);
    document.getElementById("demo").textContent =
      "Erro ao buscar leilões: " + error.message;
  }
}

async function registrarInteresse(leilaoId) {
  try {
    const response = await fetch(`${API_URL}/interesse`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        leilao_id: leilaoId,
        cliente_id: clienteId,
      }),
    });

    const data = await response.json();
    alert(data.message);

    if (data.success) {
      buscaLeiloes(); // Atualizar lista
    }
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
                <p><strong>Valor Mínimo:</strong> R$ ${leilao.valor_minimo.toFixed(
                  2
                )}</p>
                <p><strong>Início:</strong> ${new Date(
                  leilao.data_inicio
                ).toLocaleString("pt-BR")}</p>
                <p><strong>Fim:</strong> ${new Date(
                  leilao.data_fim
                ).toLocaleString("pt-BR")}</p>
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
