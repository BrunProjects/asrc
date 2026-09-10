def obter_pontos_criticos(df):
    return df[df["Qualidade"].isin(["Fraco", "Ruim"])].sort_values("Mediana")

def obter_pontos_ruins(df):
    return df[df["Qualidade"] == "Ruim"].sort_values("Mediana")

def gerar_recomendacoes(df):
    recomendacoes = []

    ruins = obter_pontos_ruins(df)
    fracos = df[df["Qualidade"] == "Fraco"].sort_values("Mediana")

    for _, p in ruins.iterrows():
        recomendacoes.append(
            f"Alta prioridade: investigar a cobertura em {p['Local']} "
            f"(ID {p['ID']}), com mediana de {p['Mediana']} dBm."
        )

    for _, p in fracos.iterrows():
        recomendacoes.append(
            f"Média prioridade: monitorar {p['Local']} "
            f"(ID {p['ID']}), com mediana de {p['Mediana']} dBm."
        )

    if not recomendacoes:
        recomendacoes.append("Nenhum ponto crítico foi encontrado com os filtros atuais.")

    return recomendacoes
