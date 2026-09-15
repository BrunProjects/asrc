from pathlib import Path

import pandas as pd
import streamlit as st

from analise.classificacao import (classificar_sinal, definir_prioridade)
from analise.estatisticas import (gerar_estatisticas)
from analise.diagnostico import (obter_pontos_criticos, gerar_recomendacoes)
from graficos.graficos import (grafico_sinal, grafico_qualidade, grafico_distancia)
from componentes.sidebar import (render_sidebar)
from componentes.metricas import (render_metrics)
from componentes.selecao import (render_selected_point)
from mapa.mapa import (gerar_mapa_interativo)

BASE = Path(__file__).parent

st.set_page_config(
    page_title="Análise da Rede Wi-Fi",
    layout="wide",
)


@st.cache_data
def carregar_dados():

    df = pd.read_csv(
        BASE / "dados" / "wifi.csv"
    )

    df.columns = (
        df.columns
        .str.strip()
        .str.replace("*", "", regex=False)
    )

    if "Tipo" in df.columns:

        df["Tipo"] = (
            df["Tipo"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    colunas_numericas = [
        "Mediana",
        "Sinal_Distante",
        "Variacao",
    ]

    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce",
            )

    df["Qualidade"] = (
        df["Mediana"]
        .apply(classificar_sinal)
    )

    df["Prioridade"] = (
        df["Qualidade"]
        .apply(definir_prioridade)
    )

    return df


@st.cache_data
def carregar_pontos_mapa():

    caminho = BASE / "dados" / "pontos_mapa.csv"

    pontos = pd.read_csv(
        caminho,
        encoding="utf-8-sig",
        sep=",",
    )

    return pontos


# ============================================================
# CARREGAMENTO
# ============================================================

df = carregar_dados()

pontos_mapa = carregar_pontos_mapa()


# ============================================================
# CABEÇALHO
# ============================================================

st.title(
    "Análise de Cobertura da Rede Wi-Fi"
)

st.caption(
    "Diagnóstico da intensidade, qualidade e distribuição "
    "do sinal nos pontos avaliados do campus."
)


# ============================================================
# FILTROS
# ============================================================

qualidades, tipos, tendencias = render_sidebar()


# Normaliza os tipos selecionados no sidebar
tipos = [
    str(tipo)
    .strip()
    .upper()
    .replace("MEDIÇÃO", "MEDICAO")
    for tipo in tipos
]


# ============================================================
# FILTRO
# ============================================================

df_filtrado = df[
    df["Qualidade"].isin(qualidades)
    & df["Tipo"].isin(tipos)
    & df["Tendencia"].isin(tendencias)
].copy()


# ============================================================
# ESTATÍSTICAS
# ============================================================

estatisticas = gerar_estatisticas(
    df_filtrado
)

render_metrics(
    estatisticas
)


st.divider()


# ============================================================
# MAPA
# ============================================================

st.subheader(
    "Mapa de cobertura"
)

mapa = gerar_mapa_interativo(
    df_filtrado,
    pontos_mapa,
    BASE / "mapa" / "campus.png",
)

evento = st.plotly_chart(
    mapa,
    width="stretch",
    on_select="rerun",
    selection_mode="points",
    key="mapa_wifi",
)

render_selected_point(
    evento,
    df_filtrado,
)


st.divider()


# ============================================================
# ANÁLISE DOS DADOS
# ============================================================

st.subheader(
    "Análise dos dados"
)


st.plotly_chart(
    grafico_sinal(df_filtrado),
    width="stretch",
)


g1, g2 = st.columns(2)


with g1:

    st.plotly_chart(
        grafico_qualidade(df_filtrado),
        width="stretch",
    )


with g2:

    st.plotly_chart(
        grafico_distancia(df_filtrado),
        width="stretch",
    )


st.divider()


# ============================================================
# PONTOS CRÍTICOS
# ============================================================

st.subheader(
    "Pontos que merecem atenção"
)


criticos = obter_pontos_criticos(
    df_filtrado
)


if not criticos.empty:

    st.dataframe(
        criticos[
            [
                "ID",
                "Local",
                "Tipo",
                "Mediana",
                "Sinal_Distante",
                "Variacao",
                "Tendencia",
                "Qualidade",
                "Prioridade",
            ]
        ],
        width="stretch",
        hide_index=True,
    )

else:

    st.success(
        "Nenhum ponto crítico encontrado "
        "com os filtros atuais."
    )


st.divider()


# ============================================================
# DIAGNÓSTICO
# ============================================================

st.subheader(
    "Diagnóstico"
)


recomendacoes = gerar_recomendacoes(
    df_filtrado
)


if recomendacoes:

    for recomendacao in recomendacoes:

        st.write(
            f"- {recomendacao}"
        )

else:

    st.info(
        "Nenhuma recomendação específica "
        "foi gerada para os pontos selecionados."
    )


# ============================================================
# RECOMENDAÇÕES GERAIS
# ============================================================

st.subheader(
    "Recomendações gerais"
)

st.write(
    "Antes de instalar novos APs, recomenda-se verificar "
    "o posicionamento, potência de transmissão, obstáculos "
    "físicos, canais utilizados e qual AP está atendendo "
    "cada área crítica."
)

st.write(
    "As áreas classificadas como ruins devem ser priorizadas "
    "para uma nova medição após qualquer ajuste realizado "
    "na infraestrutura."
)


st.divider()


# ============================================================
# DADOS COMPLETOS
# ============================================================

with st.expander(
    "Visualizar dados completos"
):

    st.dataframe(
        df_filtrado,
        width="stretch",
        hide_index=True,
    )