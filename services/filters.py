import pandas as pd
from datetime import timedelta
from config import LATENCY_METRICS, FILTROS_TEMPO

class HeatmapFilter:
    @staticmethod
    def filter_by_time(df: pd.DataFrame, tempo_selecionado:  str) -> pd.DataFrame:
        if df.empty or 'timestamp' not in df.columns:
            return df

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
        agora = pd.Timestamp.now(tz='UTC')
        if tempo_selecionado in FILTROS_TEMPO:
            return df[df['timestamp'] >= agora - FILTROS_TEMPO[tempo_selecionado]]
        return df

    @staticmethod
    def get_available_network(df: pd.DataFrame, connection_type: str) -> list:
        if df.empty:
            return []

        coluna = 'connected_ssid' if connection_type == 'Wi-Fi' else 'mobile_operator'
        if coluna in df.columns:
                return df[coluna].dropna().unique().tolist()

    @staticmethod
    def filter_by_network(df: pd.DataFrame, connection_type:str, networks_selecionadas: list)-> pd.DataFrame:
        if df.empty or len(networks_selecionadas) == 0:
            return pd.DataFrame()
        coluna = 'connected_ssid' if connection_type == 'Wi-Fi' else 'mobile_operator'
        return df[df[coluna].isin(networks_selecionadas)].copy()

    @staticmethod
    def normalizar_pesos(df: pd.DataFrame, metrica: str) -> pd.DataFrame:
        df = df.copy()
        min_val = df[metrica].min()
        max_val = df[metrica].max()

        if max_val == min_val:
            df["peso_norm"] = 0.5
            return df

        is_latency = metrica in LATENCY_METRICS
        if is_latency:
            df["peso_norm"] = 0.1 + 0.9 * (1.0 - (df[metrica] - min_val) / (max_val - min_val))
        else:
            df["peso_norm"] = 0.1 + 0.9 * ((df[metrica] - min_val) / (max_val - min_val))
        return df