let baseUrl = "http://localhost:4444/";
let clienteId = getUserIdFromSessionStorage();
let eventSource = null;
let leiloesAtivos = [];
let leiloesEncerrados = [];

// Inicialização
window.onload = function () {
    document.getElementById('userId').textContent = clienteId.substring(0, 8) + '...';
    conectarSSE();
    carregarLeiloes();
    carregarLeiloesEncerrados();
    
    // Auto-refresh a cada 10 segundos
    setInterval(() => {
        const tabAtiva = document.querySelector('.tab-content.active').id;
        if (tabAtiva === 'tab-ativos') {
            carregarLeiloes();
        } else {
            carregarLeiloesEncerrados();
        }
    }, 10000);
};

let leilaoSelecionado = null;

// Abrir modal de lance
// Abrir modal de lance
function abrirModalLance(leilao) {
    console.log('Abrindo modal para leilão:', leilao);
    
    leilaoSelecionado = leilao;
    
    const modal = document.getElementById('modalLance');
    if (!modal) {
        console.error('Modal não encontrado!');
        return;
    }
    
    const infoModal = document.getElementById('leilao-info-modal');
    if (!infoModal) {
        console.error('Container de info do modal não encontrado!');
        return;
    }
    
    infoModal.innerHTML = `
        <h3>${leilao.nome}</h3>
        <p>${leilao.descricao}</p>
        <div class="info-row">
            <span class="info-label">Valor Mínimo:</span>
            <span class="valor-destaque">R$ ${leilao.valor_inicial}</span>
        </div>
    `;
    
    modal.classList.add('show');
    
    const inputValor = document.getElementById('valorLance');
    if (inputValor) {
        inputValor.value = '';
        setTimeout(() => inputValor.focus(), 100);
    }
    
    console.log('Modal aberto!');
}

// Fechar modal
function fecharModal() {
    document.getElementById('modalLance').classList.remove('show');
    leilaoSelecionado = null;
}

// Renderizar leilões ativos
function renderLeiloesAtivos(lista) {
    const container = document.getElementById('leiloes-ativos');
    
    if (lista.length === 0) {
        renderEmpty(container.id, 'Nenhum leilão ativo no momento', 'fire');
        return;
    }
    
    container.innerHTML = '';
    
    lista.forEach(leilao => {
        const card = document.createElement('div');
        card.className = 'leilao-card';
        card.innerHTML = `
            <div class="leilao-header">
                <span class="leilao-id">#${leilao.id}</span>
                <span class="leilao-status status-ativo">
                    <i class="fas fa-circle"></i> Ativo
                </span>
            </div>
            
            <h3 class="leilao-title">${leilao.nome || 'Sem título'}</h3>
            <p class="leilao-descricao">${leilao.descricao || 'Sem descrição'}</p>
            
            <div class="leilao-info">
                <div class="info-row">
                    <span class="info-label"><i class="fas fa-tag"></i> Valor Inicial:</span>
                    <span class="info-value valor-destaque">R$ ${leilao.valor_inicial}</span>
                </div>
                <div class="info-row">
                    <span class="info-label"><i class="far fa-clock"></i> Início:</span>
                    <span class="info-value">${formatarData(leilao.inicio)}</span>
                </div>
                <div class="info-row">
                    <span class="info-label"><i class="far fa-calendar"></i> Término:</span>
                    <span class="info-value">${formatarData(leilao.fim)}</span>
                </div>
            </div>
            
            <div class="leilao-tempo">
                <i class="fas fa-hourglass-half"></i> ${calcularTempoRestante(leilao.fim)}
            </div>
            
            <div class="leilao-actions">
                <button class="btn btn-success" onclick="event.stopPropagation(); registrarInteresse(${leilao.id})">
                    <i class="fas fa-bell"></i> Registrar Interesse
                </button>
                <button class="btn btn-danger" onclick="event.stopPropagation(); cancelarInteresse(${leilao.id})">
                    <i class="fas fa-bell-slash"></i> Cancelar
                </button>
            </div>
        `;
        
        // Adicionar evento de clique no card (exceto nos botões)
        card.addEventListener('click', function(e) {
            // Não abrir modal se clicar nos botões
            if (!e.target.closest('.leilao-actions')) {
                abrirModalLance(leilao);
            }
        });
        
        container.appendChild(card);
    });
}

// Enviar lance
async function enviarLance(event) {
    event.preventDefault();
    
    if (!leilaoSelecionado) return;
    
    const valor = parseFloat(document.getElementById('valorLance').value);
    
    try {
        const res = await fetch(`${baseUrl}lance`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                leilao_id: leilaoSelecionado.id,
                user_id: clienteId,
                valor: valor
            }),
        });
        
        const data = await res.json();
        
        if (data.success) {
            mostrarNotificacao('Sucesso!', 'Lance enviado com sucesso!', 'success');
            fecharModal();
            carregarLeiloes();
        } else {
            mostrarNotificacao('Erro', data.message || 'Lance não aceito', 'error');
        }
    } catch (e) {
        console.error("Erro:", e);
        mostrarNotificacao('Erro', 'Erro ao enviar lance: ' + e.message, 'error');
    }
}

// Fechar modal ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('modalLance');
    if (event.target === modal) {
        fecharModal();
    }
}

// Funções de Tab
function switchTab(tab) {
    // Atualizar botões
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    event.target.closest('.tab-button').classList.add('active');
    
    // Atualizar conteúdo
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(`tab-${tab}`).classList.add('active');
    
    // Carregar dados
    if (tab === 'ativos') {
        carregarLeiloes();
    } else {
        carregarLeiloesEncerrados();
    }
}

// Buscar leilões ativos
async function carregarLeiloes() {
    try {
        const res = await fetch(`${baseUrl}leiloes`);
        const body = await res.json();
        leiloesAtivos = body.leiloes || [];
        renderLeiloesAtivos(leiloesAtivos);
        atualizarBadge('ativos', leiloesAtivos.length);
    } catch (e) {
        console.error("Erro ao buscar leilões:", e);
        renderEmpty('leiloes-ativos', 'Erro ao carregar leilões');
    }
}

// Buscar leilões encerrados
async function carregarLeiloesEncerrados() {
    try {
        const res = await fetch(`${baseUrl}leiloes/encerrados`);
        const body = await res.json();
        leiloesEncerrados = body.leiloes || [];
        renderLeiloesEncerrados(leiloesEncerrados);
        atualizarBadge('encerrados', leiloesEncerrados.length);
    } catch (e) {
        console.error("Erro ao buscar leilões encerrados:", e);
        renderEmpty('leiloes-encerrados', 'Erro ao carregar leilões');
    }
}

// Renderizar leilões ativos
function renderLeiloesAtivos(lista) {
    const container = document.getElementById('leiloes-ativos');
    
    if (lista.length === 0) {
        renderEmpty(container.id, 'Nenhum leilão ativo no momento', 'fire');
        return;
    }
    
    container.innerHTML = lista.map(leilao => `
        <div class="leilao-card">
            <div class="leilao-header">
                <span class="leilao-id">#${leilao.id}</span>
                <span class="leilao-status status-ativo">
                    <i class="fas fa-circle"></i> Ativo
                </span>
            </div>
            
            <h3 class="leilao-title">${leilao.nome || 'Sem título'}</h3>
            <p class="leilao-descricao">${leilao.descricao || 'Sem descrição'}</p>
            
            <div class="leilao-info">
                <div class="info-row">
                    <span class="info-label"><i class="fas fa-tag"></i> Valor Inicial:</span>
                    <span class="info-value valor-destaque">R$ ${leilao.valor_inicial}</span>
                </div>
                <div class="info-row">
                    <span class="info-label"><i class="far fa-clock"></i> Início:</span>
                    <span class="info-value">${formatarData(leilao.inicio)}</span>
                </div>
                <div class="info-row">
                    <span class="info-label"><i class="far fa-calendar"></i> Término:</span>
                    <span class="info-value">${formatarData(leilao.fim)}</span>
                </div>
            </div>
            
            <div class="leilao-tempo">
                <i class="fas fa-hourglass-half"></i> ${calcularTempoRestante(leilao.fim)}
            </div>
            
            <div class="leilao-actions">
                <button class="btn btn-success" onclick="registrarInteresse(${leilao.id})">
                    <i class="fas fa-bell"></i> Registrar Interesse
                </button>
                <button class="btn btn-danger" onclick="cancelarInteresse(${leilao.id})">
                    <i class="fas fa-bell-slash"></i> Cancelar
                </button>
            </div>
        </div>
    `).join('');
}

// Renderizar leilões encerrados
function renderLeiloesEncerrados(lista) {
    const container = document.getElementById('leiloes-encerrados');
    
    if (lista.length === 0) {
        renderEmpty(container.id, 'Nenhum leilão encerrado ainda', 'history');
        return;
    }
    
    container.innerHTML = lista.map(leilao => `
        <div class="leilao-card encerrado">
            <div class="leilao-header">
                <span class="leilao-id">#${leilao.id}</span>
                <span class="leilao-status status-encerrado">
                    <i class="fas fa-check-circle"></i> Encerrado
                </span>
            </div>
            
            <h3 class="leilao-title">${leilao.nome || 'Sem título'}</h3>
            <p class="leilao-descricao">${leilao.descricao || 'Sem descrição'}</p>
            
            <div class="leilao-info">
                <div class="info-row">
                    <span class="info-label"><i class="fas fa-tag"></i> Valor Inicial:</span>
                    <span class="info-value">R$ ${leilao.valor_inicial}</span>
                </div>
                <div class="info-row">
                    <span class="info-label"><i class="far fa-calendar-check"></i> Encerrado em:</span>
                    <span class="info-value">${formatarData(leilao.fim)}</span>
                </div>
            </div>
            
            ${leilao.vencedor ? `
                <div class="vencedor-info">
                    <strong><i class="fas fa-trophy"></i> Vencedor:</strong> ${leilao.vencedor} <br>
                    <strong><i class="fas fa-dollar-sign"></i> Lance Vencedor:</strong> R$ ${leilao.valor_final}
                </div>
            ` : `
                <div class="leilao-tempo">
                    <i class="fas fa-info-circle"></i> Sem lances vencedores
                </div>
            `}
        </div>
    `).join('');
}

// Renderizar estado vazio
function renderEmpty(containerId, mensagem, icon = 'inbox') {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-${icon}"></i>
            <h3>${mensagem}</h3>
            <p>Volte mais tarde ou crie um novo leilão</p>
        </div>
    `;
}

// Atualizar badge
function atualizarBadge(tipo, count) {
    const badge = document.getElementById(`badge-${tipo}`);
    if (badge) {
        badge.textContent = count;
    }
}

// Registrar interesse
async function registrarInteresse(leilaoId) {
    try {
        const res = await fetch(`${baseUrl}registrar_interesse`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ leilao_id: leilaoId, cliente_id: clienteId }),
        });
        
        if (!res.ok) throw new Error(`Erro HTTP: ${res.status}`);
        
        const data = await res.json();
        mostrarNotificacao('Sucesso!', data.message, 'success');
    } catch (e) {
        console.error("Erro:", e);
        mostrarNotificacao('Erro', 'Erro ao registrar interesse: ' + e.message, 'error');
    }
}

// Cancelar interesse
async function cancelarInteresse(leilaoId) {
    try {
        const res = await fetch(`${baseUrl}cancelar_interesse`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ leilao_id: leilaoId, cliente_id: clienteId }),
        });
        
        const data = await res.json();
        mostrarNotificacao('Sucesso!', data.message, 'success');
    } catch (e) {
        mostrarNotificacao('Erro', 'Erro ao cancelar interesse', 'error');
    }
}

// Conectar SSE
function conectarSSE() {
    eventSource = new EventSource(`${baseUrl}stream?channel=${clienteId}`);
    
    eventSource.addEventListener('lance', function(event) {
        try {
            const data = JSON.parse(event.data);
            mostrarNotificacao(
                'Novo Lance!',
                `Leilão #${data.leilao_id}: R$ ${data.valor}`,
                'info'
            );
            carregarLeiloes();
        } catch (e) {
            console.error("Erro ao processar dados SSE:", e);
        }
    });
    
    eventSource.addEventListener('vencedor', function(event) {
        try {
            const data = JSON.parse(event.data);
            mostrarNotificacao('Leilão Encerrado!', data.message, 'success');
            
            if (data.link_pagamento) {
                exibirLinkPagamento(data.link_pagamento, data.leilao_id, data.valor);
            }
            
            carregarLeiloes();
            carregarLeiloesEncerrados();
        } catch (e) {
            console.error("Erro ao processar notificação de vencedor:", e);
        }
    });
    
    eventSource.onerror = function (event) {
        console.error("Erro na conexão SSE:", event);
        atualizarStatusSSE(false);
        
        if (eventSource.readyState === EventSource.CLOSED) {
            setTimeout(() => conectarSSE(), 5000);
        }
    };
    
    eventSource.onopen = function () {
        console.log("SSE conectado.");
        atualizarStatusSSE(true);
    };
}

// Atualizar status SSE
function atualizarStatusSSE(conectado) {
    const statusEl = document.getElementById('sse-status');
    const container = statusEl.parentElement;
    
    if (conectado) {
        statusEl.innerHTML = '<i class="fas fa-circle"></i> Conectado';
        container.classList.add('connected');
        container.classList.remove('disconnected');
    } else {
        statusEl.innerHTML = '<i class="fas fa-circle"></i> Desconectado';
        container.classList.remove('connected');
        container.classList.add('disconnected');
    }
}

// Exibir link de pagamento
function exibirLinkPagamento(link, leilaoId, valor) {
    const container = document.getElementById('payment-links-container');
    
    const linkDiv = document.createElement("div");
    linkDiv.className = "payment-link-box";
    linkDiv.innerHTML = `
        <h3><i class="fas fa-credit-card"></i> Pagamento do Leilão #${leilaoId}</h3>
        <p><strong>Valor:</strong> R$ ${valor}</p>
        <p><strong>Link de Pagamento:</strong></p>
        <a href="${link}" target="_blank">
            <i class="fas fa-external-link-alt"></i> Pagar Agora
        </a>
    `;
    
    container.prepend(linkDiv);
}

// Mostrar notificação (substitui alert)
function mostrarNotificacao(titulo, mensagem, tipo = 'info') {
    // Por enquanto usar alert, depois pode implementar toast/notification
    alert(`${titulo}\n${mensagem}`);
}

// Utility functions
function getUserIdFromSessionStorage() {
    let userId = sessionStorage.getItem("userId");
    if (!userId) {
        userId = crypto.randomUUID();
        sessionStorage.setItem("userId", userId);
    }
    return userId;
}

function formatarData(isoString) {
    if (!isoString) return 'N/A';
    const data = new Date(isoString);
    return data.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function calcularTempoRestante(fimIso) {
    const agora = new Date();
    const fim = new Date(fimIso);
    const diff = fim - agora;
    
    if (diff <= 0) return 'Encerrado';
    
    const dias = Math.floor(diff / (1000 * 60 * 60 * 24));
    const horas = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutos = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    if (dias > 0) return `${dias}d ${horas}h ${minutos}m restantes`;
    if (horas > 0) return `${horas}h ${minutos}m restantes`;
    return `${minutos}m restantes`;
}

// Função antiga mantida para compatibilidade
function buscaLeiloes() {
    carregarLeiloes();
}