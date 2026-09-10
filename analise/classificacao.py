def classificar_sinal(dbm):
    if dbm >= -50:
        return "Excelente"
    if dbm >= -60:
        return "Bom"
    if dbm >= -67:
        return "Aceitável"
    if dbm >= -70:
        return "Fraco"
    return "Ruim"


def definir_prioridade(qualidade):
    if qualidade in ("Excelente", "Bom"):
        return "Baixa"
    if qualidade == "Aceitável":
        return "Monitorar"
    if qualidade == "Fraco":
        return "Média"
    return "Alta"
