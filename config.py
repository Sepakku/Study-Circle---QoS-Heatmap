from datetime import timedelta

METRIC_LABELS = {
    "download_mbps": "Download (Mbps)",
    "upload_mbps": "Upload (Mbps)",
    "ping": "Ping (ms)",
    "jitter": "Jitter (ms)",
}

GRADIENT_HEATMAP = {
    0.2: "blue",
    0.4: "cyan",
    0.6: "lime",
    0.8: "yellow",
    1.0: "red",
}

LATENCY_METRICS = {
    "ping", "jitter"
}

UNIDADES = {
    "download_mbps": "Mbps",
    "upload_mbps": "Mbps",
    "ping": "ms",
    "jitter": "ms",
}

FILTROS_TEMPO = {
    "Última hora": timedelta(hours=1),
    "Últimas 24 horas": timedelta(days=1),
    "Últimos 7 dias": timedelta(days=7),
    "Últimos 30 dias": timedelta(days=30),
    }