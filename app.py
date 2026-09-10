from pathlib import Path

import pandas as pd
import streamlit as st

from analise.classificacao import classificar_sinal, definir_prioridade
from analise.estatisticas import gerar_estatisticas
from analise.diagnostico import obter_pontos_criticos, gerar_recomendacoes
from mapa.mapa import gerar_mapa_interativo
from graficos.graficos import grafico_sinal, grafico_qualidade, grafico_distancia


BASE = Path(__file__).parent


st.set_page_config(
    page_title="Análise da Rede Wi-Fi",
    layout="wide",
)


@st.cache_data
def carregar_dados():
    df = pd.read_csv(BASE / "dados" / "wifi.csv")
    df["Qualidade"] = df["Mediana"].apply(classificar_sinal)
    df["Prioridade"] = df["Qualidade"].apply(definir_prioridade)
    return df


@st.cache_data
def carregar_pontos_mapa():
    return pd.read_csv(BASE / "dados" / "pontos_mapa.csv")


df = carregar_dados()
pontos_mapa = carregar_pontos_mapa()


st.title("Análise de Cobertura da Rede Wi-Fi")
st.caption(
    "Diagnóstico da intensidade, qualidade e distribuição do sinal "
    "nos pontos avaliados do campus."
)


# Filtros
st.sidebar.header("Filtros")

qualidades = st.sidebar.multiselect(
    "Qualidade",
    ["Excelente", "Bom", "Aceitável", "Fraco", "Ruim"],
    default=["Excelente", "Bom", "Aceitável", "Fraco", "Ruim"],
)

tipos = st.sidebar.multiselect(
    "Tipo",
    ["AP", "Medicao"],
    default=["AP", "Medicao"],
    format_func=lambda x: "Medição" if x == "Medicao" else x,
)

tendencias = st.sidebar.multiselect(
    "Tendência",
    ["Direita", "Esquerda"],
    default=["Direita", "Esquerda"],
)


df_filtrado = df[
    df["Qualidade"].isin(qualidades)
    & df["Tipo"].isin(tipos)
    & df["Tendencia"].isin(tendencias)
].copy()


estatisticas = gerar_estatisticas(df_filtrado)

# Cards
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Pontos analisados", estatisticas["total_pontos"])
c2.metric("APs", estatisticas["total_aps"])
c3.metric("Medições", estatisticas["total_medicoes"])
c4.metric("Mediana geral", f'{estatisticas["mediana_geral"]:.0f} dBm')
c5.metric("Pontos ruins", estatisticas["total_ruim"])


st.divider()


# Mapa
st.subheader("Mapa de cobertura")

mapa = gerar_mapa_interativo(
    df_filtrado,
    pontos_mapa,
    BASE / "mapa" / "campus.png",
)

evento = st.plotly_chart(
    mapa,
    use_container_width=True,
    on_select="rerun",
    selection_mode="points",
    key="mapa_wifi",
)


# Seleção pelo clique
ponto_selecionado = None

try:
    indices = evento.selection.point_indices
    if indices:
        ponto_selecionado = df_filtrado.iloc[indices[0]]
except Exception:
    pass


if ponto_selecionado is not None:
    st.success(f"Ponto {ponto_selecionado['ID']} selecionado")

    d1, d2, d3, d4 = st.columns(4)
    d1.write(f"**Local:** {ponto_selecionado['Local']}")
    d2.write(f"**Mediana:** {ponto_selecionado['Mediana']} dBm")
    d3.write(f"**Qualidade:** {ponto_selecionado['Qualidade']}")
    d4.write(f"**Prioridade:** {ponto_selecionado['Prioridade']}")



st.divider()


# Gráficos
st.subheader("Análise dos dados")

st.plotly_chart(
    grafico_sinal(df_filtrado),
    use_container_width=True,
)

g1, g2 = st.columns(2)

with g1:
    st.plotly_chart(
        grafico_qualidade(df_filtrado),
        use_container_width=True,
    )

with g2:
    st.plotly_chart(
        grafico_distancia(df_filtrado),
        use_container_width=True,
    )


st.divider()


# Pontos críticos
st.subheader("Pontos que merecem atenção")
criticos = obter_pontos_criticos(df_filtrado)

if not criticos.empty:
    st.dataframe(
        criticos[
            [
                "ID", "Local", "Tipo", "Mediana",
                "Sinal_Distante", "Variacao",
                "Tendencia", "Qualidade", "Prioridade"
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.success("Nenhum ponto crítico encontrado com os filtros atuais.")


st.divider()


# Diagnóstico e recomendações
st.subheader("Diagnóstico")

for recomendacao in gerar_recomendacoes(df_filtrado):
    st.write(f"- {recomendacao}")


st.subheader("Recomendações gerais")

st.write(
    "Antes de instalar novos APs, recomenda-se verificar o posicionamento, "
    "potência de transmissão, obstáculos físicos, canais utilizados e "
    "qual AP está atendendo cada área crítica."
)

st.write(
    "As áreas classificadas como ruins devem ser priorizadas para uma nova "
    "medição após qualquer ajuste realizado na infraestrutura."
)


st.divider()


with st.expander("Visualizar dados completos"):
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
    )
