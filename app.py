import streamlit as st
from datetime import date, datetime
import pandas as pd

import data as db
import charts
from profiles import (
    PROFILES,
    CATEGORY_TO_PROFILE_GROUP,
    TODAS_CATEGORIAS_GASTO,
    CATEGORIAS_FIXAS,
    CATEGORIAS_VARIAVEIS,
    CATEGORIAS_INVESTIMENTOS,
    DIAGNOSTICOS,
)

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Caixinhas 💰",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
    }
    .metric-label { font-size: 13px; color: #aaa; margin-bottom: 4px; }
    .metric-value { font-size: 28px; font-weight: 700; }
    .verde { color: #4CAF50; }
    .vermelho { color: #F44336; }
    .azul { color: #2196F3; }
    .roxo { color: #9C27B0; }
    .status-ok { color: #4CAF50; font-weight: 600; }
    .status-atencao { color: #FF9800; font-weight: 600; }
    .status-alto { color: #F44336; font-weight: 600; }
    .motivacao {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        border-left: 4px solid #42A5F5;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 12px 0;
        font-size: 14px;
        color: #E3F2FD;
    }
    div[data-testid="stSidebar"] { background-color: #12121f; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Inicializar estado ──────────────────────────────────────────────────────
if "caixinhas_data" not in st.session_state:
    st.session_state["caixinhas_data"] = {}

dados = db.load_data()

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("💰 Caixinhas")
    st.caption("Controle financeiro para brasileiros na Europa")
    st.divider()

    # Seletor de perfil
    st.subheader("👤 Seu Perfil")
    perfil_opcoes = {k: v["nome"] for k, v in PROFILES.items()}
    perfil_key = st.selectbox(
        "Escolha seu perfil:",
        options=list(perfil_opcoes.keys()),
        format_func=lambda k: perfil_opcoes[k],
        key="perfil_key",
        help="O perfil define os percentuais recomendados exibidos no dashboard.",
    )
    st.caption(PROFILES[perfil_key]["descricao"])
    st.divider()

    # Seletor de mês/ano
    st.subheader("📅 Período")
    hoje = date.today()
    col_m, col_y = st.columns(2)
    with col_m:
        mes = st.selectbox(
            "Mês",
            options=list(range(1, 13)),
            index=hoje.month - 1,
            format_func=lambda m: [
                "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"
            ][m - 1],
        )
    with col_y:
        ano = st.selectbox(
            "Ano",
            options=list(range(hoje.year - 3, hoje.year + 2)),
            index=3,
        )
    mes_key = db.get_month_key(ano, mes)
    st.divider()

    # Navegação
    st.subheader("🗺️ Navegação")
    tela = st.radio(
        "Ir para:",
        options=["dashboard", "historico", "saude"],
        format_func=lambda t: {
            "dashboard": "📊 Dashboard do Mês",
            "historico": "📈 Histórico",
            "saude": "🏥 Saúde Financeira",
        }[t],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Dados mantidos na sessão do browser")


# ══════════════════════════════════════════════════════════════════════════════
# TELA: DASHBOARD DO MÊS
# ══════════════════════════════════════════════════════════════════════════════
def tela_dashboard():
    meses_pt = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ]
    st.header(f"📊 {meses_pt[mes - 1]} de {ano}")

    resumo = db.get_month_summary(dados, mes_key)
    total_ent = resumo["total_entradas"]
    total_gas = resumo["total_gastos"]
    saldo = resumo["saldo"]
    por_cat = resumo["por_categoria"]

    investido = por_cat.get("Investimentos", 0) + por_cat.get("Reserva de Emergência", 0)
    pct_inv = (investido / total_ent * 100) if total_ent > 0 else 0

    # ── Cards de resumo ──────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Total de Entradas</div>'
            f'<div class="metric-value verde">€ {total_ent:,.2f}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Total de Gastos</div>'
            f'<div class="metric-value vermelho">€ {total_gas:,.2f}</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        cor_saldo = "verde" if saldo >= 0 else "vermelho"
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Saldo do Mês</div>'
            f'<div class="metric-value {cor_saldo}">€ {saldo:,.2f}</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">% Investido / Poupado</div>'
            f'<div class="metric-value azul">{pct_inv:.1f}%</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Mensagem de motivação ────────────────────────────────────────────────
    if saldo > 0 and pct_inv >= PROFILES[perfil_key]["percentuais"].get("Investimentos", 0):
        msg = "🎉 Excelente! Você está investindo acima do recomendado. Continue construindo seu patrimônio na Europa!"
    elif saldo > 0:
        msg = "💪 Bom trabalho! Você fechou o mês no positivo. Cada euro poupado é um passo a mais na sua jornada."
    elif saldo == 0:
        msg = "⚖️ Mês equilibrado! Tente guardar um pouco mais no próximo mês — cada euro conta."
    else:
        msg = "🧭 Mês difícil, mas você não está sozinho. Revise os gastos e trace um plano para o próximo mês."

    st.markdown(f'<div class="motivacao">{msg}</div>', unsafe_allow_html=True)

    # ── Gráficos ─────────────────────────────────────────────────────────────
    col_g1, col_g2 = st.columns([1, 1.3])
    with col_g1:
        st.plotly_chart(
            charts.donut_gastos(por_cat),
            use_container_width=True,
        )
    with col_g2:
        st.plotly_chart(
            charts.barras_real_vs_recomendado(por_cat, total_ent, perfil_key),
            use_container_width=True,
        )

    st.divider()

    # ── Formulários de registro ──────────────────────────────────────────────
    col_form1, col_form2 = st.columns(2)

    with col_form1:
        st.subheader("➕ Registrar Entrada")
        with st.form("form_entrada", clear_on_submit=True):
            desc_e = st.text_input("Descrição", placeholder="Ex: Salário de Abril")
            valor_e = st.number_input("Valor (€)", min_value=0.01, step=10.0, format="%.2f")
            data_e = st.date_input("Data", value=date(ano, mes, 1))
            if st.form_submit_button("💚 Adicionar Entrada", use_container_width=True):
                if desc_e and valor_e > 0:
                    db.add_entrada(dados, mes_key, desc_e, valor_e, str(data_e))
                    st.success(f"Entrada de € {valor_e:.2f} registrada!")
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")

    with col_form2:
        st.subheader("➖ Registrar Gasto")
        with st.form("form_gasto", clear_on_submit=True):
            desc_g = st.text_input("Descrição", placeholder="Ex: Aluguel de Abril")
            cat_g = st.selectbox("Categoria", options=TODAS_CATEGORIAS_GASTO)
            valor_g = st.number_input("Valor (€)", min_value=0.01, step=10.0, format="%.2f")
            data_g = st.date_input("Data", value=date(ano, mes, 1))
            if st.form_submit_button("❤️ Adicionar Gasto", use_container_width=True):
                if desc_g and valor_g > 0:
                    db.add_gasto(dados, mes_key, desc_g, cat_g, valor_g, str(data_g))
                    st.success(f"Gasto de € {valor_g:.2f} em '{cat_g}' registrado!")
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")

    st.divider()

    # ── Lista de transações ──────────────────────────────────────────────────
    st.subheader("📋 Transações do Mês")

    mes_data = dados.get(mes_key, {"entradas": [], "gastos": []})
    entradas_lista = mes_data.get("entradas", [])
    gastos_lista = mes_data.get("gastos", [])

    tab_ent, tab_gas = st.tabs([
        f"💚 Entradas ({len(entradas_lista)})",
        f"❤️ Gastos ({len(gastos_lista)})",
    ])

    with tab_ent:
        if entradas_lista:
            for i, t in enumerate(sorted(entradas_lista, key=lambda x: x["data"], reverse=True)):
                col_a, col_b, col_c, col_d = st.columns([2, 3, 2, 1])
                col_a.write(t["data"])
                col_b.write(t["descricao"])
                col_c.markdown(f"**<span style='color:#4CAF50'>€ {t['valor']:,.2f}</span>**", unsafe_allow_html=True)
                if col_d.button("🗑️", key=f"del_e_{i}", help="Remover"):
                    original_idx = entradas_lista.index(t)
                    db.delete_transaction(dados, mes_key, "entradas", original_idx)
                    st.rerun()
        else:
            st.info("Nenhuma entrada registrada neste mês.")

    with tab_gas:
        if gastos_lista:
            for i, t in enumerate(sorted(gastos_lista, key=lambda x: x["data"], reverse=True)):
                col_a, col_b, col_c, col_d, col_e = st.columns([2, 3, 2, 2, 1])
                col_a.write(t["data"])
                col_b.write(t["descricao"])
                col_c.write(t["categoria"])
                col_d.markdown(f"**<span style='color:#F44336'>€ {t['valor']:,.2f}</span>**", unsafe_allow_html=True)
                if col_e.button("🗑️", key=f"del_g_{i}", help="Remover"):
                    original_idx = gastos_lista.index(t)
                    db.delete_transaction(dados, mes_key, "gastos", original_idx)
                    st.rerun()
        else:
            st.info("Nenhum gasto registrado neste mês.")


# ══════════════════════════════════════════════════════════════════════════════
# TELA: HISTÓRICO
# ══════════════════════════════════════════════════════════════════════════════
def tela_historico():
    st.header("📈 Histórico Financeiro")

    historico = db.get_history(dados, last_n=12)

    if not historico:
        st.info("Nenhum dado encontrado. Comece registrando entradas e gastos no Dashboard.")
        return

    # Gráfico de linha
    st.plotly_chart(charts.linha_saldo_historico(historico), use_container_width=True)

    # Gráfico de barras empilhadas
    st.plotly_chart(charts.barras_empilhadas_historico(historico), use_container_width=True)

    st.divider()

    # Tabela resumo
    st.subheader("📊 Tabela Resumo Mensal")
    rows = []
    for h in reversed(historico):
        total_inv = h.get("por_categoria", {}).get("Investimentos", 0) + h.get("por_categoria", {}).get("Reserva de Emergência", 0)
        pct_inv = (total_inv / h["total_entradas"] * 100) if h["total_entradas"] > 0 else 0
        rows.append({
            "Mês": h["mes"],
            "Entradas (€)": f"€ {h['total_entradas']:,.2f}",
            "Gastos (€)": f"€ {h['total_gastos']:,.2f}",
            "Saldo (€)": f"€ {h['saldo']:,.2f}",
            "% Investido": f"{pct_inv:.1f}%",
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TELA: SAÚDE FINANCEIRA
# ══════════════════════════════════════════════════════════════════════════════
def tela_saude():
    meses_pt = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ]
    st.header(f"🏥 Saúde Financeira — {meses_pt[mes - 1]} de {ano}")

    resumo = db.get_month_summary(dados, mes_key)
    total_ent = resumo["total_entradas"]
    por_cat = resumo["por_categoria"]
    perfil = PROFILES[perfil_key]
    percentuais_rec = perfil["percentuais"]

    if total_ent <= 0:
        st.warning("Registre entradas no Dashboard para ver a análise de saúde financeira.")
        return

    st.markdown(f"**Perfil selecionado:** {perfil['nome']}")
    st.markdown(f"**Renda total do mês:** € {total_ent:,.2f}")
    st.divider()

    # Consolidar categorias reais em grupos de perfil
    grupos_reais: dict[str, float] = {}
    for cat, valor in por_cat.items():
        grupo = CATEGORY_TO_PROFILE_GROUP.get(cat)
        if grupo:
            grupos_reais[grupo] = grupos_reais.get(grupo, 0.0) + valor

    diagnosticos_gerados = []

    for grupo, rec_pct in percentuais_rec.items():
        valor_real = grupos_reais.get(grupo, 0.0)
        pct_real = (valor_real / total_ent * 100) if total_ent > 0 else 0

        if pct_real <= rec_pct:
            status_html = '<span class="status-ok">✅ OK</span>'
            status_str = "ok"
        elif pct_real <= rec_pct * 1.15:
            status_html = '<span class="status-atencao">⚠️ Atenção</span>'
            status_str = "atencao"
        else:
            status_html = '<span class="status-alto">🔴 Acima</span>'
            status_str = "alto"

        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
        col1.markdown(f"**{grupo}**")
        col2.markdown(f"€ {valor_real:,.2f}")
        col3.markdown(f"{pct_real:.1f}% da renda")
        col4.markdown(f"Rec.: {rec_pct:.0f}%")
        col5.markdown(status_html, unsafe_allow_html=True)

        # Diagnóstico
        if grupo in DIAGNOSTICOS:
            chave = "alto" if status_str == "alto" or status_str == "atencao" else "ok"
            msg = DIAGNOSTICOS[grupo][chave].format(pct=pct_real, rec=rec_pct)
            if status_str != "ok":
                diagnosticos_gerados.append((grupo, msg, status_str))

    st.divider()

    # Diagnóstico automático consolidado
    st.subheader("💬 Diagnóstico Automático")

    if not diagnosticos_gerados:
        st.markdown(
            '<div class="motivacao">🌟 Parabéns! Todas as categorias estão dentro do recomendado para o seu perfil. '
            'Você está construindo um futuro sólido na Europa. Continue assim!</div>',
            unsafe_allow_html=True,
        )
    else:
        for grupo, msg, status in diagnosticos_gerados:
            cor = "#FF9800" if status == "atencao" else "#F44336"
            st.markdown(
                f'<div style="border-left: 4px solid {cor}; background: #1e1e2e; '
                f'border-radius: 8px; padding: 12px 16px; margin: 8px 0; font-size: 14px;">'
                f'<strong>{grupo}</strong><br>{msg}</div>',
                unsafe_allow_html=True,
            )

    # Pontuação de saúde geral
    st.divider()
    st.subheader("🎯 Pontuação de Saúde Financeira")

    total_grupos = len(percentuais_rec)
    grupos_ok = total_grupos - len(diagnosticos_gerados)
    score = int((grupos_ok / total_grupos) * 100) if total_grupos > 0 else 100

    if score >= 80:
        cor_score = "#4CAF50"
        label_score = "Excelente"
        emoji_score = "🌟"
    elif score >= 60:
        cor_score = "#FF9800"
        label_score = "Bom"
        emoji_score = "👍"
    elif score >= 40:
        cor_score = "#FF5722"
        label_score = "Regular"
        emoji_score = "⚠️"
    else:
        cor_score = "#F44336"
        label_score = "Precisa de Atenção"
        emoji_score = "🚨"

    st.markdown(
        f'<div style="text-align:center; padding: 24px; background: #1e1e2e; border-radius: 12px;">'
        f'<div style="font-size: 64px; font-weight: 800; color: {cor_score};">{score}</div>'
        f'<div style="font-size: 18px; color: {cor_score};">{emoji_score} {label_score}</div>'
        f'<div style="font-size: 13px; color: #888; margin-top: 8px;">'
        f'{grupos_ok} de {total_grupos} categorias dentro do recomendado</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Roteamento ───────────────────────────────────────────────────────────────
if tela == "dashboard":
    tela_dashboard()
elif tela == "historico":
    tela_historico()
elif tela == "saude":
    tela_saude()
