import base64
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image


def carregar_mapa(caminho="mapa/campus.png"):
    caminho = Path(caminho)
    imagem = Image.open(caminho)
    return imagem


def _imagem_base64(caminho):
    caminho = Path(caminho)
    extensao = caminho.suffix.lower().replace(".", "")
    mime = "jpeg" if extensao in ("jpg", "jpeg") else "png"
    dados = base64.b64encode(caminho.read_bytes()).decode("utf-8")
    return f"data:image/{mime};base64,{dados}"


def gerar_mapa_interativo(df, pontos_mapa, caminho_imagem="mapa/campus.png"):
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size

    dados = df.merge(pontos_mapa, on="ID", how="inner").copy()

    # Os pontos ficam invisíveis/quase transparentes porque os marcadores
    # já estão desenhados na imagem original. Eles servem para hover e clique.
    dados["Cor"] = dados["Tendencia"].map({
        "Direita": "green",
        "Esquerda": "red"
    }).fillna("gray")

    fig = go.Figure()

    fig.add_layout_image(
        dict(
            source=_imagem_base64(caminho_imagem),
            xref="x",
            yref="y",
            x=0,
            y=altura,
            sizex=largura,
            sizey=altura,
            sizing="stretch",
            opacity=1,
            layer="below",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dados["X"],
            y=altura - dados["Y"],
            mode="markers",
            customdata=dados[
                ["ID", "Local", "Tipo", "Mediana", "Sinal_Distante",
                 "Variacao", "Tendencia", "Qualidade", "Prioridade"]
            ].values,
            marker=dict(
                size=30,
                color=dados["Cor"],
                opacity=0.18,
                line=dict(width=2),
            ),
            hovertemplate=(
                "<b>ID %{customdata[0]}</b><br>"
                "%{customdata[1]}<br>"
                "Mediana: %{customdata[3]} dBm<br>"
                "Distante: %{customdata[4]} dBm<br>"
                "Qualidade: %{customdata[7]}<br>"
                "Tendência: %{customdata[6]}<br>"
                "<extra>Clique para selecionar</extra>"
            ),
            name="Pontos",
        )
    )

    fig.update_xaxes(
        range=[0, largura],
        showgrid=False,
        zeroline=False,
        visible=False,
        fixedrange=True,
    )
    fig.update_yaxes(
        range=[0, altura],
        showgrid=False,
        zeroline=False,
        visible=False,
        fixedrange=True,
        scaleanchor="x",
        scaleratio=1,
    )

    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        showlegend=False,
        dragmode=False,
    )

    return fig
