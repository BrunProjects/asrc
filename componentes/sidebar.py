import streamlit as st

def render_sidebar():
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

    return qualidades, tipos, tendencias