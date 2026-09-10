import streamlit as st

def render_selected_point(evento, df_filtrado):
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