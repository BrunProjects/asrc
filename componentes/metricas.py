import streamlit as st

def render_metrics(estatisticas):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Pontos analisados", estatisticas["total_pontos"])
    c2.metric("APs", estatisticas["total_aps"])
    c3.metric("Medições", estatisticas["total_medicoes"])
    c4.metric("Mediana geral", f'{estatisticas["mediana_geral"]:.0f} dBm')
    c5.metric("Pontos ruins", estatisticas["total_ruim"])