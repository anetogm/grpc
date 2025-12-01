// Script para fazer lance
const API_URL = "http://localhost:3000/api";

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
    const response = await fetch(`${API_URL}/lance`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        leilao_id: parseInt(leilaoId),
        user_id: userId,
        valor: parseFloat(valorLance),
      }),
    });

    const data = await response.json();

    if (data.success) {
      document.getElementById("resultado").textContent = `✓ ${
        data.message
      } (Válido: ${data.valido ? "Sim" : "Não"})`;
      document.getElementById("resultado").style.color = "green";
    } else {
      document.getElementById("resultado").textContent = `✗ ${data.message}`;
      document.getElementById("resultado").style.color = "red";
    }
  } catch (error) {
    console.error("Erro ao fazer lance:", error);
    document.getElementById("resultado").textContent = "Erro: " + error.message;
    document.getElementById("resultado").style.color = "red";
  }
}
