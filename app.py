import streamlit as st
from data.cache import CacheRepository
from services.filters import HeatmapFilter
from ui import sidebar
from ui.map import render_map
from ui.metrics import render_metrics_cards

st.set_page_config(page_title="Heatmap de Conectividade", layout='wide')

def main():
    st.title("StudyCicle - QoS Heatmap")

    if st.sidebar.button('Renovar Dados'):
        st.cache_data.clear()

    wifi_df = CacheRepository.get_wifi_cache()
    mobile_df = CacheRepository.get_mobile_cache()

    tipo_conexao = sidebar.render_connection_type()
    base_df = wifi_df if tipo_conexao == "Wi-Fi" else mobile_df

    opcoes_rede = HeatmapFilter.get_available_network(base_df, tipo_conexao)
    redes_selecionadas = sidebar.render_network_selector(tipo_conexao, opcoes_rede)
    filtro_tempo = sidebar.render_time_filter()
    metrica, raio, blur = sidebar.render_heatmap_settings()

    df = HeatmapFilter.filter_by_network(base_df, tipo_conexao, redes_selecionadas)
    df = HeatmapFilter.filter_by_time(df, filtro_tempo)

    render_metrics_cards(df, metrica)
    st.markdown('---')

    if not df.empty and metrica in df.columns:
        df = HeatmapFilter.normalizar_pesos(df, metrica)
        redes_str = "-".join(sorted(redes_selecionadas)) if redes_selecionadas else "none"
        cache_key = f"{tipo_conexao}_{redes_str}_{metrica}_{raio}_{blur}_{filtro_tempo}"
        render_map(df, metrica, raio, blur, key_suffix=cache_key)
    else:
        st.error("Nenhum dado encontrado para a combinação de rede, tempo ou métrica selecionada.")

if __name__ == "__main__":
    main()