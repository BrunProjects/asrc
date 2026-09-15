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

    extensao = (
        caminho.suffix
        .lower()
        .replace(".", "")
    )

    mime = (
        "jpeg"
        if extensao in ("jpg", "jpeg")
        else "png"
    )

    dados = base64.b64encode(
        caminho.read_bytes()
    ).decode("utf-8")

    return f"data:image/{mime};base64,{dados}"


def gerar_mapa_interativo(
    df,
    pontos_mapa,
    caminho_imagem="mapa/campus.png",
):

    # ========================================================
    # IMAGEM
    # ========================================================

    imagem = Image.open(caminho_imagem)

    largura, altura = imagem.size


    # ========================================================
    # CÓPIAS DOS DATAFRAMES
    # ========================================================

    df = df.copy()
    pontos_mapa = pontos_mapa.copy()


    # ========================================================
    # NORMALIZAÇÃO DAS COLUNAS
    # ========================================================

    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.replace("*", "", regex=False)
        .str.strip()
    )

    pontos_mapa.columns = (
        pontos_mapa.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.replace("*", "", regex=False)
        .str.strip()
    )


    # ========================================================
    # VERIFICAÇÃO DAS COLUNAS
    # ========================================================

    if "ID" not in df.columns:

        raise ValueError(
            "O wifi.csv não possui a coluna 'ID'. "
            f"Colunas encontradas: {list(df.columns)}"
        )


    if "ID" not in pontos_mapa.columns:

        raise ValueError(
            "O pontos_mapa.csv não possui a coluna 'ID'. "
            f"Colunas encontradas: {list(pontos_mapa.columns)}"
        )


    if "X" not in pontos_mapa.columns:

        raise ValueError(
            "O pontos_mapa.csv não possui a coluna 'X'. "
            f"Colunas encontradas: {list(pontos_mapa.columns)}"
        )


    if "Y" not in pontos_mapa.columns:

        raise ValueError(
            "O pontos_mapa.csv não possui a coluna 'Y'. "
            f"Colunas encontradas: {list(pontos_mapa.columns)}"
        )


    # ========================================================
    # NORMALIZAÇÃO DOS IDs
    # ========================================================

    df["ID"] = pd.to_numeric(
        df["ID"],
        errors="coerce",
    )

    pontos_mapa["ID"] = pd.to_numeric(
        pontos_mapa["ID"],
        errors="coerce",
    )


    # Remove IDs inválidos
    df = df.dropna(
        subset=["ID"]
    ).copy()

    pontos_mapa = pontos_mapa.dropna(
        subset=["ID"]
    ).copy()


    # Converte para inteiro
    df["ID"] = df["ID"].astype(int)

    pontos_mapa["ID"] = (
        pontos_mapa["ID"]
        .astype(int)
    )


    # ========================================================
    # NORMALIZAÇÃO DAS COORDENADAS
    # ========================================================

    pontos_mapa["X"] = pd.to_numeric(
        pontos_mapa["X"],
        errors="coerce",
    )

    pontos_mapa["Y"] = pd.to_numeric(
        pontos_mapa["Y"],
        errors="coerce",
    )


    pontos_mapa = pontos_mapa.dropna(
        subset=["X", "Y"]
    ).copy()


    # ========================================================
    # MERGE
    # ========================================================

    dados = df.merge(
        pontos_mapa[
            ["ID", "X", "Y"]
        ],
        on="ID",
        how="inner",
    ).copy()


    # ========================================================
    # VERIFICAÇÃO DO MERGE
    # ========================================================

    if dados.empty:

        raise ValueError(
            "Nenhum ID do wifi.csv foi encontrado "
            "no pontos_mapa.csv."
        )


    # ========================================================
    # CORES
    # ========================================================

    dados["Cor"] = (
        dados["Tendencia"]
        .map({
            "Direita": "green",
            "Esquerda": "red",
        })
        .fillna("gray")
    )


    # ========================================================
    # FIGURA
    # ========================================================

    fig = go.Figure()


    # ========================================================
    # IMAGEM DO CAMPUS
    # ========================================================

    fig.add_layout_image(
        dict(
            source=_imagem_base64(
                caminho_imagem
            ),
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


    # ========================================================
    # PONTOS
    # ========================================================

    fig.add_trace(
        go.Scatter(
            x=dados["X"],
            y=altura - dados["Y"],

            mode="markers+text",

            text=dados["ID"],

            textposition="middle center",

            textfont=dict(
                color="white",
                size=11,
            ),

            customdata=dados[
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
            ].values,

            marker=dict(
                size=25,
                color=dados["Cor"],
                opacity=1,
                line=dict(
                    width=2,
                    color="black",
                ),
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


    # ========================================================
    # EIXO X
    # ========================================================

    fig.update_xaxes(
        range=[0, largura],
        showgrid=False,
        zeroline=False,
        visible=False,
        fixedrange=True,
    )


    # ========================================================
    # EIXO Y
    # ========================================================

    fig.update_yaxes(
        range=[0, altura],
        showgrid=False,
        zeroline=False,
        visible=False,
        fixedrange=True,
        scaleanchor="x",
        scaleratio=1,
    )


    # ========================================================
    # LAYOUT
    # ========================================================

    fig.update_layout(
        height=650,

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),

        hovermode="closest",

        showlegend=False,
        dragmode=False,
    )


    return fig