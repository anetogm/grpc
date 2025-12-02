// Lances via gRPC-Web (Envoy)
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

async function fazerLance() {
  const leilaoId = document.getElementById("leilaoId").value;
  const valorLance = document.getElementById("valorLance").value;
  const userId = getUserIdFromSessionStorage();

  if (!leilaoId || !valorLance) {
    document.getElementById("resultado").textContent =
      "Preencha todos os campos.";
    return;
  }

  try {
    const req = new GrpcClient.EnviarLanceRequest();
    req.setLeilaoId(parseInt(leilaoId));
    req.setUserId(userId);
    req.setValor(parseFloat(valorLance));

    client.enviarLance(req, {}, (err, resp) => {
      if (err) {
        console.error("Erro ao fazer lance:", err.message);
        document.getElementById("resultado").textContent =
          "Erro: " + err.message;
        document.getElementById("resultado").style.color = "red";
        return;
      }
      if (resp.getSuccess()) {
        document.getElementById(
          "resultado"
        ).textContent = `✓ ${resp.getMessage()} (Válido: ${
          resp.getValido() ? "Sim" : "Não"
        })`;
        document.getElementById("resultado").style.color = "green";
      } else {
        document.getElementById(
          "resultado"
        ).textContent = `✗ ${resp.getMessage()}`;
        document.getElementById("resultado").style.color = "red";
      }
    });
  } catch (error) {
    console.error("Erro ao fazer lance:", error);
    document.getElementById("resultado").textContent = "Erro: " + error.message;
    document.getElementById("resultado").style.color = "red";
  }
}
