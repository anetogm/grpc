// Cadastro via gRPC-Web (Envoy)
const client = new proto.gateway.GatewayServiceClient(
  "http://localhost:8080",
  null,
  null
);

function nowForDatetimeLocal() {
  const now = new Date();
  now.setSeconds(0, 0);
  const tzOffsetMin = now.getTimezoneOffset();
  const local = new Date(now.getTime() - tzOffsetMin * 60000);
  return local.toISOString().slice(0, 16);
}

async function cadastrarLeilao(event) {
  event.preventDefault();

  const item = document.getElementById("item").value;
  const descricao = document.getElementById("descricao").value;
  const valor_inicial = parseFloat(
    document.getElementById("valor_inicial").value
  );
  const inicio = document.getElementById("inicio").value;
  const fim = document.getElementById("fim").value;

  try {
    const req = new proto.leilao.CriarLeilaoRequest();
    req.setNome(item);
    req.setDescricao(descricao);
    req.setValorInicial(valor_inicial);
    req.setInicio(inicio);
    req.setFim(fim);

    client.criarLeilao(req, {}, (err, resp) => {
      if (err) {
        console.error("Erro ao cadastrar leilão:", err.message);
        alert("Erro ao cadastrar leilão: " + err.message);
        return;
      }
      if (resp.getSuccess()) {
        document.getElementById("successMessage").style.display = "block";
        document.getElementById("cadastraLeilaoForm").reset();
        setTimeout(() => {
          window.location.href = "/";
        }, 2000);
      } else {
        alert("Erro: " + resp.getMessage());
      }
    });
  } catch (error) {
    console.error("Erro ao cadastrar leilão:", error);
    alert("Erro ao cadastrar leilão: " + error.message);
  }
}

// Configurar data/hora padrão
window.addEventListener("DOMContentLoaded", () => {
  const inicioInput = document.getElementById("inicio");
  const fimInput = document.getElementById("fim");

  if (inicioInput && !inicioInput.value) {
    inicioInput.value = nowForDatetimeLocal();
  }

  if (fimInput && !fimInput.value) {
    const futuro = new Date();
    futuro.setHours(futuro.getHours() + 24);
    const tzOffsetMin = futuro.getTimezoneOffset();
    const localFuturo = new Date(futuro.getTime() - tzOffsetMin * 60000);
    fimInput.value = localFuturo.toISOString().slice(0, 16);
  }

  const form = document.getElementById("cadastraLeilaoForm");
  if (form) {
    form.addEventListener("submit", cadastrarLeilao);
  }
});
