import plotly.express as px
import plotly.graph_objects as go


def grafico_sinal(df):
    dados = df.sort_values("Mediana", ascending=True)
    fig = px.bar(
        dados,
        x="Mediana",
        y="Local",
        orientation="h",
        text="Mediana",
        hover_data=["ID", "Qualidade", "Tipo", "Tendencia"],
        title="Intensidade do sinal por local",
    )
    for limite in [-50, -60, -67, -70]:
        fig.add_vline(x=limite, line_dash="dash")
    fig.update_layout(xaxis_title="Sinal (dBm)", yaxis_title="")
    return fig


def grafico_qualidade(df):
    ordem = ["Excelente", "Bom", "Aceitável", "Fraco", "Ruim"]
    contagem = df["Qualidade"].value_counts().reindex(ordem, fill_value=0)
    fig = go.Figure(
        go.Bar(
            x=contagem.index,
            y=contagem.values,
            text=contagem.values,
            textposition="auto",
        )
    )
    fig.update_layout(
        title="Distribuição da qualidade do sinal",
        xaxis_title="Qualidade",
        yaxis_title="Quantidade de pontos",
    )
    return fig


def grafico_distancia(df):
    fig = go.Figure()
    fig.add_bar(
        x=df["Local"],
        y=df["Mediana"],
        name="2–4 metros",
        customdata=df[["ID", "Qualidade"]].values,
        hovertemplate=(
            "ID %{customdata[0]}<br>%{x}<br>"
            "2–4 m: %{y} dBm<br>Qualidade: %{customdata[1]}"
            "<extra></extra>"
        ),
    )
    fig.add_bar(
        x=df["Local"],
        y=df["Sinal_Distante"],
        name="10–30 metros",
    )
    fig.update_layout(
        title="Comparação do sinal conforme a distância",
        xaxis_title="Local",
        yaxis_title="Sinal (dBm)",
        barmode="group",
    )
    return fig
