def gerar_estatisticas(df):
    return {
        "total_pontos": len(df),
        "total_aps": len(df[df["Tipo"] == "AP"]),
        "total_medicoes": len(df[df["Tipo"] == "MEDICAO"]),
        "mediana_geral": df["Mediana"].median(),
        "melhor_sinal": df["Mediana"].max(),
        "pior_sinal": df["Mediana"].min(),
        "total_excelente": len(df[df["Qualidade"] == "Excelente"]),
        "total_bom": len(df[df["Qualidade"] == "Bom"]),
        "total_aceitavel": len(df[df["Qualidade"] == "Aceitável"]),
        "total_fraco": len(df[df["Qualidade"] == "Fraco"]),
        "total_ruim": len(df[df["Qualidade"] == "Ruim"]),
    }
