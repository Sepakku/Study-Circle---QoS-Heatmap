# ui/map_component.py
import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import st_folium
from config import METRIC_LABELS, UNIDADES, GRADIENT_HEATMAP, LATENCY_METRICS

def render_map(df, metric, radius, blur, key_suffix):
    if df.empty or metric not in df.columns:
        st.error("Nenhum dado encontrado para a seleção.")
        return df

    # Create the base map
    m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=18, tiles='OpenStreetMap')
    
    # Add HeatMap
    dados_heat = df[["latitude", "longitude", "peso_norm"]].values.tolist()
    HeatMap(
        dados_heat,
        radius=radius,
        blur=blur,
        min_opacity=0.3,
        gradient=GRADIENT_HEATMAP,
    ).add_to(m)

    # Calculate Legend values
    min_val = df[metric].min()
    max_val = df[metric].max()
    is_latency = metric in LATENCY_METRICS
    legend_colors = "linear-gradient(to right, red, yellow, lime, cyan, blue)" if is_latency else "linear-gradient(to right, blue, cyan, lime, yellow, red)"

    # Build an absolute positioned HTML block for inside the Folium map
    legend_html = f"""
        <div style="
            position: absolute; 
            bottom: 30px; 
            left: 20px; 
            z-index: 9999; 
            background-color: rgba(255, 255, 255, 0.9); 
            padding: 10px; 
            border-radius: 8px; 
            border: 1px solid grey;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
            width: 200px;
            color: black;
        ">
            <div style="font-weight: bold; font-size: 14px; margin-bottom: 4px;">Métrica: {METRIC_LABELS.get(metric, metric)}</div>
            <div style="background: {legend_colors}; height: 14px; border-radius: 4px; width: 100%;"></div>
            <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 2px;">
                <span>{min_val:.1f} {UNIDADES.get(metric, '')}</span>
                <span>{max_val:.1f} {UNIDADES.get(metric, '')}</span>
            </div>
        </div>
    """
    
    # Inject the HTML directly into the Folium map element
    m.get_root().html.add_child(folium.Element(legend_html))

    # Render map
    st_folium(m, use_container_width=True, height=500, key=f"mapa_{key_suffix}")