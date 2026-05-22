import streamlit as st
import anthropic
import hashlib
from pathlib import Path
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Índio Jurídico Prime",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── AUTENTICAÇÃO ─────────────────────────────────────────────
def _hash(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()

USUARIOS = {
    "wagner":   {"hash": _hash("Ind!o@W2026"),  "nome": "Wagner Antonelli",  "cargo": "CEO",           "admin": True},
    "carolina": {"hash": _hash("Ind!o@C2026"),  "nome": "Carolina Antonelli","cargo": "Sócia",         "admin": False},
    "david":    {"hash": _hash("Ind!o@D2026"),  "nome": "David Antonelli",   "cargo": "Sócio",         "admin": False},
    "roberta":  {"hash": _hash("Ind!o@R2026"),  "nome": "Dra. Roberta",      "cargo": "Advogada",      "admin": False},
    "cristina": {"hash": _hash("Ind!o@Cris26"), "nome": "Cristina",          "cargo": "Contabilidade", "admin": False},
    "nicolas":  {"hash": _hash("Ind!o@N2026"),  "nome": "Nicolás",           "cargo": "Diretor",       "admin": False},
}

def get_all_users():
    """Mescla usuários fixos + extras cadastrados pelo admin (salvos nos secrets)."""
    todos = dict(USUARIOS)
    try:
        extras = st.secrets.get("extra_users", {})
        import json
        for login, dados_str in extras.items():
            try:
                dados = json.loads(dados_str) if isinstance(dados_str, str) else dict(dados_str)
                dados.setdefault("admin", False)
                todos[login] = dados
            except Exception:
                pass
    except Exception:
        pass
    return todos

def is_admin():
    u = st.session_state.get("usuario", "")
    return get_all_users().get(u, {}).get("admin", False)

# ─── SYSTEM PROMPT ────────────────────────────────────────────
SYSTEM_PROMPT = """Você é o ÍNDIO JURÍDICO PRIME — sistema de inteligência jurídica estratégica de elite do Grupo Supermercado Índio (10 lojas no Rio Grande do Sul).

Você atua como analista jurídico sênior apoiando:
- Wagner Antonelli (CEO e sócio-gestor)
- Carolina e David (sócios)
- Dra. Roberta (advogada interna — valida e protocola todas as peças)
- Cristina (contabilidade — interface tributária)

Seu padrão intelectual é o das grandes bancas jurídicas brasileiras. Pense como advogado sênior estratégico.

REGRA ABSOLUTA: Toda peça produzida é MINUTA TÉCNICA — revisão obrigatória por advogado habilitado. NUNCA substitui o jurídico. NUNCA inventa jurisprudência, número de processo ou ementa.

═══════════════════════════════════════════
ENTIDADES DO GRUPO
═══════════════════════════════════════════
Empresas: WCA | NIMABE | MNB Participações | WD Construtora | Giovana SC | Glacial | Magna | Laiza | Rubimar Antonelli | SET Monitoramento | AG Capital | CWD Veículos

Lojas ativas (10):
1-MATRIZ(Guaíba) | 2-Jardim Guaíba | 3-Coronel Nassuca | 6-Centro Eldorado(Eldorado do Sul) | 7-Guaíba Passo Fundo | 9-São Jerônimo | 10-Arroio dos Ratos | 11-Charqueadas 1ºMaio | 12-Charqueadas 2 | 13-Guaíba Centro

Advogados externos: Dr. Rafael Mattos (tributário) | Houer Gebras (tributário) | MSH Advocacia (tributário) | Dr. Flávio | Dr. Valmor | Dr. Gilmar/Idea Fiscal (consultoria fiscal)

═══════════════════════════════════════════
FLUXO COMPLETO — ANÁLISE DE PROCESSO (9 ETAPAS)
═══════════════════════════════════════════
Ao receber qualquer processo, documento, notificação ou situação jurídica, execute SEMPRE:

ETAPA 1 — IDENTIFICAÇÃO: Número CNJ | tribunal/vara | área | partes + advogados | valor causa + atualizado | fase | prazo fatal | risco imediato (bloqueio/penhora?) | entidade/loja envolvida

ETAPA 2 — RESUMO EXECUTIVO (máx. 10 linhas):
CASO: | ÁREA: | ENTIDADE: | VALOR EM RISCO: R$ | PRAZO FATAL: | FASE: | RISCO IMEDIATO: | AÇÃO URGENTE:

ETAPA 3 — LINHA DO TEMPO: fato gerador → notificações → audiências → decisões → prazos futuros

ETAPA 4 — DIAGNÓSTICO: Pontos FORTES / FRACOS da empresa | Pontos FRÁGEIS da parte contrária | Provas existentes vs faltantes | Riscos (financeiro, bloqueio, penhora, pessoal) | Chance de acordo % | Chance de êxito %

ETAPA 5 — ANÁLISE DE FUROS (PRIORITÁRIA): Varredura em: prescrição/decadência | ilegitimidade de parte | ausência de nexo/dano | nulidade processual | excesso de cálculo | falta de prova | incompetência | cerceamento de defesa | inconsistência documental | coisa julgada | litispendência.
Classificar: GRAVE (muda resultado) | MÉDIO (reduz valor) | LEVE (reforço) | OPORTUNIDADE | SEM UTILIDADE

ETAPA 6 — JURISPRUDÊNCIA: Buscar por ordem: STF → STJ → TST/TRT4 → TJRS → TRF4 → CARF
Classificar: MUITO FORTE | BOA | ÚTIL | FRACA | CONTRÁRIA (enfrentar diretamente)
NUNCA inventar decisão, número ou ementa.

ETAPA 7 — ESTRATÉGIA: Tese principal | Tese subsidiária | Tese de redução de valor | Análise acordo (R$ acordo vs R$ risco condenação) | Tese recursal

ETAPA 8 — MINUTA DA PEÇA: Endereçamento → Qualificação → Síntese fática → Preliminares → Mérito (com jurisprudência) → Pedidos hierarquizados → Requerimento de provas → Fechamento formal (espaço para OAB/advogado)

ETAPA 9 — CHECKLIST FINAL: Documentos faltantes | Provas a anexar | Prazo fatal + data de protocolo | Risco se inerte | Próximos passos | Validação Dra. Roberta

═══════════════════════════════════════════
URGÊNCIA (prazo < 48h)
═══════════════════════════════════════════
Alertar: "🚨 URGÊNCIA — PRAZO EM [X] HORAS"
Executar apenas Etapas 1 + 2 + 8. Minuta imediata.

═══════════════════════════════════════════
PROTOCOLO — ANÁLISE DE CONTRATOS
═══════════════════════════════════════════
Verificar: prazo/vigência | multas | reajuste unilateral | responsabilidade sócios | foro RS | exclusividade | renovação automática | cláusulas leoninas | LGPD
Output: mapa de risco (verde/amarelo/vermelho) + cláusulas problemáticas com redação alternativa + parecer: assinar | negociar | recusar

═══════════════════════════════════════════
TRIBUTÁRIO — TESES ATIVAS DO GRUPO
═══════════════════════════════════════════
⚠️ ALERTA CRÍTICO Tema 1.223 STJ: NUNCA excluir PIS/COFINS da base do ICMS — autuação de alto risco.
⚠️ PRESCRIÇÃO: Créditos de 2020/2021 prescrevem em breve — acionar imediatamente.

Teses ativas:
🟢 ICMS-ST na base PIS/COFINS (Tema 1.125 STJ) — muito forte
🟢 Crédito insumos PIS/COFINS (REsp 1.221.170/STJ) — energia, diesel, fretes
🟢 Verbas indenizatórias INSS — terço férias, aviso prévio, 15 dias auxílio-doença
🟢 ADC 49 — sem ICMS na transferência entre filiais
🟢 Crédito ICMS energia elétrica — câmaras frias, padaria, açougue
🟡 INSS sobre horas extras — ajuizar urgente (prescrição)
🟡 IRPJ/CSLL sobre PIS/COFINS (LP) — ajuizar urgente (STJ julgando)
🟡 TUSD/TUST na base ICMS energia (Tema 986 STJ)
🟡 Subvenções ICMS — exclusão base IRPJ (pós-Lei 14.789/2023)
🟡 JCP/JSCP — dedução IRPJ/CSLL (Lucro Real)

Via de recuperação: PER/DCOMP Web (teses consolidadas) | Judicial (teses em discussão)

═══════════════════════════════════════════
COMPLIANCE TRABALHISTA — CHECKLIST POR LOJA
═══════════════════════════════════════════
Verificar: ponto eletrônico homologado | horas extras no limite | banco de horas com CCT/ACT | adicionais corretos | PPRA/PCMSO/LTCAT atualizados | CIPA constituída | E-Social em dia | cotas PCD e Aprendiz | TRCT em prazo | CAT emitida em acidentes

Red flags: colaborador sem registro | jornada >10h sem compensação | rescisão sem TRCT | acidente sem CAT | laudo NR desatualizado

═══════════════════════════════════════════
FONTES DE JURISPRUDÊNCIA
═══════════════════════════════════════════
STF: jurisprudencia.stf.jus.br
STJ: scon.stj.jus.br/SCON | Temas: processo.stj.jus.br/repetitivos
TST: tst.jus.br/sumulas
TRT4: trt4.jus.br (trabalhista RS — principal)
TJRS: tjrs.jus.br/site/jurisprudencia
TRF4: jurisprudencia.trf4.jus.br
CARF: carf.fazenda.gov.br/sincon
DataJud CNJ: api-publica.datajud.cnj.jus.br (91 tribunais)

═══════════════════════════════════════════
PEÇAS SUPORTADAS
═══════════════════════════════════════════
Contestação trabalhista/cível | Impugnação de cálculo | Embargos à execução | Exceção de pré-executividade | Recurso ordinário | Apelação cível | Defesa administrativa tributária | Impugnação auto de infração | Agravo de instrumento | Acordo trabalhista | Notificação extrajudicial | Proposta de acordo | Memoriais | Contrarrazões

═══════════════════════════════════════════
MATRIZ DE ESCALAÇÃO
═══════════════════════════════════════════
Bloqueio de conta → peça liberatória em 24h — Dra. Roberta URGENTE
Prazo < 48h → fluxo urgência
Valor > R$ 100k → estratégia com externo especialista — Wagner decide
Auto de infração tributário → Cristina + tributarista externo
Acordo > R$ 50k → aprovação Wagner antes de propor
Processo criminal → advogado criminal imediatamente

═══════════════════════════════════════════
REGRAS ABSOLUTAS
═══════════════════════════════════════════
1. NUNCA inventar jurisprudência, número de processo ou ementa
2. NUNCA afirmar tese vencedora sem grau de risco
3. NUNCA esconder risco relevante da diretoria
4. NUNCA orientar conduta ilícita
5. SEMPRE calcular prazo fatal antes de responder
6. SEMPRE indicar documentos críticos faltantes
7. SEMPRE apresentar impacto em R$ para Wagner
8. SEMPRE indicar validação obrigatória da Dra. Roberta

═══════════════════════════════════════════
PADRÃO DE RESPOSTA
═══════════════════════════════════════════
- Peças jurídicas: formal, técnico, pedidos claros e hierarquizados
- Resumos para diretoria: executivo, direto, valor em R$, risco em %, prazo em data
- Análises de risco: linguagem clara para não-advogados
- Evitar: texto genérico, tese fraca sem base, juridiquês excessivo

Data atual: """ + datetime.now().strftime("%d/%m/%Y") + """
Sistema confidencial e proprietário — Grupo Supermercado Índio"""

# ─── ESTILOS CSS ──────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0D1B2A 0%, #1B2A4A 50%, #0D1B2A 100%);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebar"] {
        background: rgba(13,27,42,0.95) !important;
        border-right: 1px solid rgba(230,81,0,0.3) !important;
    }

    /* CARD DE LOGIN */
    .login-card {
        max-width: 440px; margin: 40px auto;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-top: 4px solid #E65100;
        border-radius: 20px; padding: 40px 44px 36px;
        backdrop-filter: blur(16px);
        box-shadow: 0 24px 64px rgba(0,0,0,0.5);
    }
    .brand-title {
        font-size: 30px; font-weight: 900; color: #FFFFFF;
        letter-spacing: 1px; line-height: 1.1;
    }
    .brand-title span { color: #E65100; }
    .brand-sub {
        font-size: 13px; color: rgba(255,255,255,0.5);
        margin-top: 4px; margin-bottom: 28px;
        font-weight: 400; letter-spacing: 0.5px;
    }
    .badge-conf {
        display: inline-block; background: rgba(230,81,0,0.15);
        border: 1px solid rgba(230,81,0,0.4); border-radius: 20px;
        padding: 4px 14px; font-size: 11px; font-weight: 600;
        color: #E65100; letter-spacing: 1px; text-transform: uppercase;
        margin-bottom: 24px;
    }

    /* INPUTS */
    input[type="text"], input[type="password"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important; color: white !important;
        padding: 10px 14px !important; font-size: 14px !important;
    }
    input:focus { border-color: #E65100 !important; box-shadow: 0 0 0 2px rgba(230,81,0,0.2) !important; }

    /* BOTÃO PRIMÁRIO */
    .stButton > button {
        background: linear-gradient(135deg, #E65100, #BF360C) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;
        font-size: 14px !important; padding: 10px 28px !important;
        width: 100% !important; transition: all 0.2s !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #FF6D00, #E65100) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(230,81,0,0.4) !important;
    }

    /* HEADER DO CHAT */
    .chat-header {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-left: 4px solid #E65100;
        border-radius: 14px; padding: 18px 24px;
        margin-bottom: 20px;
        display: flex; align-items: center; gap: 16px;
    }
    .chat-title { font-size: 20px; font-weight: 800; color: #fff; }
    .chat-subtitle { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 2px; }
    .status-dot {
        width: 10px; height: 10px; background: #4CAF50;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 8px #4CAF50; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }

    /* MENSAGENS DO CHAT */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important; margin-bottom: 12px !important;
        padding: 16px !important;
    }
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: rgba(230,81,0,0.08) !important;
        border-color: rgba(230,81,0,0.2) !important;
    }
    .stChatMessage p, .stChatMessage li, .stChatMessage td {
        color: rgba(255,255,255,0.92) !important;
        font-size: 14px !important; line-height: 1.7 !important;
    }
    .stChatMessage h1,.stChatMessage h2,.stChatMessage h3 {
        color: #ffffff !important; font-weight: 700 !important;
    }
    .stChatMessage code {
        background: rgba(255,255,255,0.1) !important;
        color: #FFB74D !important; border-radius: 4px !important;
        padding: 2px 6px !important;
    }
    .stChatMessage strong { color: #FFB74D !important; font-weight: 700 !important; }
    .stChatMessage table {
        border-collapse: collapse !important; width: 100% !important;
    }
    .stChatMessage th {
        background: rgba(230,81,0,0.2) !important;
        color: #fff !important; padding: 8px 12px !important;
        font-size: 12px !important; font-weight: 600 !important;
    }
    .stChatMessage td {
        padding: 8px 12px !important; border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    }

    /* INPUT DE CHAT */
    [data-testid="stChatInputContainer"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(230,81,0,0.3) !important;
        border-radius: 14px !important; padding: 4px 8px !important;
    }
    textarea { color: white !important; background: transparent !important; }

    /* FORÇAR SIDEBAR SEMPRE VISÍVEL */
    section[data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        min-width: 280px !important;
        max-width: 380px !important;
        transform: none !important;
        opacity: 1 !important;
    }
    [data-testid="collapsedControl"] { display: none !important; }
    button[kind="header"] { display: none !important; }

    /* SIDEBAR */
    .sidebar-section {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px; padding: 14px 16px; margin-bottom: 12px;
    }
    .sidebar-label {
        font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.4);
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;
    }
    .sidebar-value { font-size: 13px; color: rgba(255,255,255,0.85); font-weight: 500; }
    .cmd-item {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px; padding: 8px 12px; margin-bottom: 6px;
        cursor: pointer; transition: all 0.2s;
    }
    .cmd-code { font-size: 11px; color: #FFB74D; font-weight: 600; font-family: monospace; }
    .cmd-desc { font-size: 11px; color: rgba(255,255,255,0.5); margin-top: 2px; }
    .aviso-legal {
        background: rgba(255,193,7,0.08); border: 1px solid rgba(255,193,7,0.2);
        border-radius: 10px; padding: 12px 14px;
        font-size: 11px; color: rgba(255,255,255,0.6); line-height: 1.5;
    }

    /* ESCONDER ELEMENTOS PADRÃO STREAMLIT */
    #MainMenu, footer, header { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ─── TELA DE LOGIN ────────────────────────────────────────────
def login_screen():
    inject_css()
    st.markdown("""
    <div class="login-card">
        <div class="brand-title">ÍNDIO <span>JURÍDICO</span></div>
        <div class="brand-sub">SISTEMA DE INTELIGÊNCIA JURÍDICA ESTRATÉGICA</div>
        <div class="badge-conf">🔒 CONFIDENCIAL — GRUPO ÍNDIO</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        with st.form("login_form", clear_on_submit=False):
            usuario = st.text_input("", placeholder="👤  Usuário", label_visibility="collapsed")
            senha   = st.text_input("", placeholder="🔑  Senha",   label_visibility="collapsed", type="password")
            entrar  = st.form_submit_button("ACESSAR SISTEMA")

        if entrar:
            u = usuario.strip().lower()
            todos = get_all_users()
            if u in todos and todos[u]["hash"] == _hash(senha):
                st.session_state.autenticado  = True
                st.session_state.usuario      = u
                st.session_state.usuario_nome = todos[u]["nome"]
                st.session_state.usuario_cargo= todos[u]["cargo"]
                st.session_state.messages     = []
                st.rerun()
            else:
                st.error("❌  Usuário ou senha incorretos.")

    st.markdown("""
    <div style='text-align:center;margin-top:32px;font-size:11px;color:rgba(255,255,255,0.25)'>
        Grupo Supermercado Índio — RS &nbsp;·&nbsp; Sistema Confidencial e Proprietário
    </div>
    """, unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.title("⚖️ ÍNDIO JURÍDICO")
        st.caption("SISTEMA DE INTELIGÊNCIA JURÍDICA")
        st.divider()

        nome  = st.session_state.get("usuario_nome", "")
        cargo = st.session_state.get("usuario_cargo", "")
        st.success(f"👤 {nome}\n\n*{cargo}*")
        st.divider()

        st.markdown("**📋 COMANDOS RÁPIDOS**")
        st.info("`analise: [doc]` — Fluxo completo 9 etapas")
        st.info("`urgente: [doc]` — Prazo < 48h")
        st.info("`furos: [processo]` — Fragilidades da parte contrária")
        st.info("`jurisprudencia: [tese]` — Busca nos tribunais")
        st.info("`tributario: [situação]` — Análise fiscal")
        st.info("`contrato: [doc]` — Análise contratual")
        st.info("`notificacao: [situação]` — Notificação extrajudicial")
        st.info("`preventivo: [loja]` — Compliance trabalhista")
        st.info("`acordo: [processo]` — Custo-benefício acordo")
        st.divider()

        st.warning("⚠️ **AVISO LEGAL**\n\nToda peça gerada é **MINUTA TÉCNICA**. Revisão obrigatória pela Dra. Roberta antes do uso.")

        # ── PAINEL ADMIN ──────────────────────────────────────────
        if is_admin():
            st.divider()
            with st.expander("⚙️ PAINEL ADMIN — Usuários"):
                todos = get_all_users()
                st.markdown("**Usuários cadastrados:**")
                for login, u in todos.items():
                    adm = " 🔑" if u.get("admin") else ""
                    st.markdown(f"- `{login}` — {u['nome']} ({u['cargo']}){adm}")

                st.markdown("---")
                st.markdown("**➕ Novo usuário:**")
                with st.form("form_novo_usuario", clear_on_submit=True):
                    novo_login = st.text_input("Login (minúsculo, sem espaço)")
                    novo_nome  = st.text_input("Nome completo")
                    novo_cargo = st.text_input("Cargo")
                    nova_senha = st.text_input("Senha", type="password")
                    novo_admin = st.checkbox("Administrador?")
                    salvar = st.form_submit_button("Criar usuário")

                if salvar:
                    import json
                    login_clean = novo_login.strip().lower().replace(" ", "")
                    if not login_clean or not novo_nome or not nova_senha:
                        st.error("Preencha login, nome e senha.")
                    elif login_clean in todos:
                        st.error(f"Login '{login_clean}' já existe.")
                    else:
                        dados = {"hash": _hash(nova_senha), "nome": novo_nome.strip(),
                                 "cargo": novo_cargo.strip(), "admin": novo_admin}
                        st.success(f"✅ {login_clean} criado!")
                        toml_atual = ""
                        try:
                            for k, v in st.secrets.get("extra_users", {}).items():
                                toml_atual += f'\n{k} = \'{v}\''
                        except Exception:
                            pass
                        bloco = f'[extra_users]{toml_atual}\n{login_clean} = \'{json.dumps(dados, ensure_ascii=False)}\''
                        st.code(bloco, language="toml")
                        st.caption("Copie → Streamlit Cloud → Settings → Secrets → cole e salve.")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚪 Sair", use_container_width=True):
                for k in ["autenticado","usuario","usuario_nome","usuario_cargo","messages"]:
                    st.session_state.pop(k, None)
                st.rerun()
        with col2:
            if st.button("🗑️ Limpar", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        st.caption("Índio Jurídico Prime v3.0 | Grupo Índio RS")

# ─── CHAT PRINCIPAL ───────────────────────────────────────────
def chat_screen():
    inject_css()
    render_sidebar()

    # Header
    st.markdown("""
    <div class="chat-header">
        <div>⚖️</div>
        <div>
            <div class="chat-title">ÍNDIO JURÍDICO PRIME &nbsp;<span class="status-dot"></span></div>
            <div class="chat-subtitle">
                Inteligência Jurídica Estratégica — Trabalhista · Cível · Tributário · Contratual · Imobiliário
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Inicializar mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mensagem de boas-vindas
    if not st.session_state.messages:
        nome = st.session_state.get("usuario_nome", "")
        with st.chat_message("assistant", avatar="⚖️"):
            st.markdown(f"""
**{nome}, sistema jurídico online.**

Estou carregado com todo o conhecimento jurídico do **Grupo Supermercado Índio**:

| Área | Capacidade |
|---|---|
| ⚖️ **Trabalhista** | Análise de processos, contestações, compliance por loja |
| 📋 **Cível** | Contratos, cobranças, notificações extrajudiciais |
| 💰 **Tributário** | 30+ teses ativas, PER/DCOMP, oportunidades de recuperação |
| 🏢 **Empresarial** | Contratos fornecedores, acordos societários |
| 🏗️ **Imobiliário** | Obras, locações, compra e venda |

**Como posso ajudar?** Cole um documento, descreva um processo ou use um dos comandos rápidos do menu lateral.
            """)

    # Histórico
    for msg in st.session_state.messages:
        avatar = "⚖️" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Digite sua pergunta ou cole o documento jurídico aqui..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Chamar API Anthropic
        with st.chat_message("assistant", avatar="⚖️"):
            with st.spinner("Analisando..."):
                try:
                    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
                    if not api_key:
                        import os
                        api_key = os.environ.get("ANTHROPIC_API_KEY", "")

                    client = anthropic.Anthropic(api_key=api_key)

                    # Montar histórico para a API
                    messages_api = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]

                    response = client.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=8096,
                        system=SYSTEM_PROMPT,
                        messages=messages_api
                    )

                    resposta = response.content[0].text
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})

                except anthropic.AuthenticationError:
                    erro = "❌ **Erro de autenticação.** Verifique a ANTHROPIC_API_KEY nos secrets do Streamlit."
                    st.error(erro)
                    st.session_state.messages.append({"role": "assistant", "content": erro})
                except Exception as e:
                    erro = f"❌ **Erro:** {str(e)}"
                    st.error(erro)
                    st.session_state.messages.append({"role": "assistant", "content": erro})

# ─── MAIN ─────────────────────────────────────────────────────
def main():
    if not st.session_state.get("autenticado"):
        login_screen()
    else:
        chat_screen()

if __name__ == "__main__":
    main()
