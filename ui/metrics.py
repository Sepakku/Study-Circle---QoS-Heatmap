import streamlit as st
import pandas as pd
from config import METRIC_LABELS, UNIDADES

def render_metrics_cards(df: pd.DataFrame, metrica: str):
    col1, col2 = st.columns(2)
    
    if not df.empty and metrica in df.columns:
        label_nome = METRIC_LABELS.get(metrica, metrica)
        unidade = UNIDADES.get(metrica, "")

        media_valor = df[metrica].mean()
        total_pontos = len(df)

        if metrica == "ping_success_rate" and media_valor <= 1.0:
            media_valor *= 100

        col1.metric(f"Média - {label_nome}", f"{media_valor:.1f} {unidade}".strip())
        col2.metric("Pontos Lidos", total_pontos)
    else:
        col1.metric("Média", "N/A")
        col2.metric("Pontos Lidos", 0)