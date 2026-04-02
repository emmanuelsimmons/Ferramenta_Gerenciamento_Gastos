import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from profiles import PROFILES, CATEGORY_TO_PROFILE_GROUP

# Paleta de cores
COLORS_CATEGORIAS = [
    "#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336",
    "#00BCD4", "#FF5722", "#8BC34A", "#E91E63", "#607D8B",
    "#FFC107", "#3F51B5",
]

COLOR_ENTRADA = "#4CAF50"
COLOR_GASTO = "#F44336"
COLOR_INVESTIMENTO = "#2196F3"
COLOR_SALDO = "#9C27B0"


def donut_gastos(por_categoria: dict, titulo: str = "Distribuição dos Gastos") -> go.Figure:
    if not por_categoria:
        fig = go.Figure()
        fig.add_annotation(text="Sem gastos registrados", x=0.5, y=0.5, showarrow=False, font_size=16)
        fig.update_layout(title=titulo, height=400)
        return fig

    labels = list(por_categoria.keys())
    values = list(por_categoria.values())

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker_colors=COLORS_CATEGORIAS[: len(labels)],
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>€ %{value:.2f}<br>%{percent}<extra></extra>",
        )
    )
    fig.update_layout(
        title=titulo,
        height=420,
        legend=dict(orientation="v", x=1.02, y=0.5),
        margin=dict(t=60, b=20, l=20, r=160),
    )
    return fig


def barras_real_vs_recomendado(
    por_categoria: dict, total_entradas: float, profile_key: str
) -> go.Figure:
    if total_entradas <= 0:
        fig = go.Figure()
        fig.add_annotation(text="Registre entradas para ver a comparação", x=0.5, y=0.5, showarrow=False, font_size=14)
        fig.update_layout(title="Real vs. Recomendado por Perfil", height=420)
        return fig

    perfil = PROFILES[profile_key]
    percentuais_rec = perfil["percentuais"]

    # Agregar categorias reais em grupos do perfil
    grupos_reais: dict[str, float] = {}
    for cat, valor in por_categoria.items():
        grupo = CATEGORY_TO_PROFILE_GROUP.get(cat)
        if grupo:
            grupos_reais[grupo] = grupos_reais.get(grupo, 0.0) + valor

    grupos = sorted(set(list(percentuais_rec.keys()) + list(grupos_reais.keys())))

    pct_real = [(grupos_reais.get(g, 0.0) / total_entradas * 100) for g in grupos]
    pct_rec = [percentuais_rec.get(g, 0) for g in grupos]

    colors_real = []
    for r, rec in zip(pct_real, pct_rec):
        if rec == 0:
            colors_real.append("#90A4AE")
        elif r <= rec:
            colors_real.append("#4CAF50")
        elif r <= rec * 1.15:
            colors_real.append("#FF9800")
        else:
            colors_real.append("#F44336")

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Real (%)",
            x=grupos,
            y=pct_real,
            marker_color=colors_real,
            hovertemplate="<b>%{x}</b><br>Real: %{y:.1f}%<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Recomendado (%)",
            x=grupos,
            y=pct_rec,
            marker_color="rgba(33,150,243,0.35)",
            marker_line_color="#2196F3",
            marker_line_width=2,
            hovertemplate="<b>%{x}</b><br>Recomendado: %{y:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"Real vs. Recomendado — Perfil: {perfil['nome']}",
        barmode="group",
        xaxis_tickangle=-35,
        yaxis_title="% da Renda",
        height=450,
        legend=dict(orientation="h", y=1.05, x=0),
        margin=dict(t=80, b=120, l=60, r=20),
    )
    return fig


def linha_saldo_historico(historico: list[dict]) -> go.Figure:
    if not historico:
        fig = go.Figure()
        fig.add_annotation(text="Sem histórico disponível", x=0.5, y=0.5, showarrow=False, font_size=16)
        fig.update_layout(title="Evolução do Saldo (últimos 12 meses)", height=400)
        return fig

    meses = [h["mes"] for h in historico]
    saldos = [h["saldo"] for h in historico]
    entradas = [h["total_entradas"] for h in historico]
    gastos = [h["total_gastos"] for h in historico]

    colors_saldo = [COLOR_ENTRADA if s >= 0 else COLOR_GASTO for s in saldos]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=meses, y=entradas, name="Entradas", mode="lines+markers",
            line=dict(color=COLOR_ENTRADA, width=2),
            hovertemplate="Entradas: € %{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=meses, y=gastos, name="Gastos", mode="lines+markers",
            line=dict(color=COLOR_GASTO, width=2),
            hovertemplate="Gastos: € %{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=meses, y=saldos, name="Saldo",
            marker_color=colors_saldo, opacity=0.6,
            hovertemplate="Saldo: € %{y:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Evolução Financeira — Últimos 12 Meses",
        yaxis_title="€",
        height=420,
        legend=dict(orientation="h", y=1.05, x=0),
        margin=dict(t=80, b=40, l=60, r=20),
        hovermode="x unified",
    )
    return fig


def barras_empilhadas_historico(historico: list[dict]) -> go.Figure:
    if not historico:
        fig = go.Figure()
        fig.add_annotation(text="Sem histórico disponível", x=0.5, y=0.5, showarrow=False, font_size=16)
        fig.update_layout(title="Gastos por Categoria ao Longo dos Meses", height=400)
        return fig

    # Coletar todas as categorias presentes
    todas_cats: set[str] = set()
    for h in historico:
        todas_cats.update(h.get("por_categoria", {}).keys())
    todas_cats_list = sorted(todas_cats)

    meses = [h["mes"] for h in historico]

    fig = go.Figure()
    for i, cat in enumerate(todas_cats_list):
        valores = [h.get("por_categoria", {}).get(cat, 0.0) for h in historico]
        fig.add_trace(
            go.Bar(
                name=cat,
                x=meses,
                y=valores,
                marker_color=COLORS_CATEGORIAS[i % len(COLORS_CATEGORIAS)],
                hovertemplate=f"<b>{cat}</b><br>€ %{{y:.2f}}<extra></extra>",
            )
        )

    fig.update_layout(
        title="Gastos por Categoria — Histórico Mensal",
        barmode="stack",
        yaxis_title="€",
        height=450,
        legend=dict(orientation="v", x=1.02, y=0.5),
        margin=dict(t=60, b=40, l=60, r=160),
    )
    return fig
