# ui/sidebar.py
import streamlit as st
from config import METRIC_LABELS

def render_connection_type() -> str:
    st.sidebar.header("Opções da Visualização")
    st.sidebar.subheader("Filtro de Rede")
    
    return st.sidebar.radio(
        "Tipo de Conexão:",
        options=["Wi-Fi", "Dados Móveis"],
        index=0,
    )

def render_network_selector(tipo_conexao: str, opcoes_disponiveis: list) -> list:
    if not opcoes_disponiveis:
        st.sidebar.warning(f"Nenhum dado encontrado para {tipo_conexao}.")
        return []

    label = "SSIDs Conectados:" if tipo_conexao == "Wi-Fi" else "Operadoras Móveis:"
    
    return st.sidebar.multiselect(
        label=label,
        options=opcoes_disponiveis,
        default=opcoes_disponiveis,
    )

def render_time_filter() -> str:
    st.sidebar.subheader("Filtro de Tempo")
    
    return st.sidebar.selectbox(
        "Exibir dados de:",
        options=[
            "Todos os tempos",
            "Última hora",
            "Últimas 24 horas",
            "Últimos 7 dias",
            "Últimos 30 dias",
        ],
        index=0,
    )

def render_heatmap_settings() -> tuple[str, int, int]:
    st.sidebar.subheader("Configurações do Heatmap")
    
    metrica = st.sidebar.radio(
        "Métrica para o Heatmap:",
        options=list(METRIC_LABELS.keys()),
        format_func=lambda x: METRIC_LABELS.get(x, x),
    )
    
    raio = st.sidebar.slider("Raio do Calor:", min_value=5, max_value=20, value=10)
    blur = st.sidebar.slider("Suavização (Blur):", min_value=1, max_value=25, value=5)
    
    return metrica, raio, blur