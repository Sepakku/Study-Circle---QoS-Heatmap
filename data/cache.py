import streamlit as st
import pandas as pd
from data.engine import get_engine


class CacheRepository:
    @st.cache_data(ttl=10800)
    def get_wifi_cache():
        engine = get_engine()
        query = '''
            SELECT me.id, me.timestamp, me.altitude, me.longitude, me.latitude, 
            me.ping, me.jitter, me.download_mbps, me.upload_mbps, wi.connected_ssid FROM measurements me
            INNER JOIN wifi_connections wi
            ON me.id = wi.measurement_id
            WHERE me.test_success IS true
        '''

        return pd.read_sql(query, engine)

    @st.cache_data(ttl=10800)
    def get_mobile_cache():
        engine = get_engine()
        query = '''
            SELECT me.id, me.timestamp, me.altitude, me.longitude, me.latitude, 
            me.ping, me.jitter, me.download_mbps, me.upload_mbps, mo.mobile_operator FROM measurements me
            INNER JOIN mobile_connections mo
            ON me.id = mo.measurement_id
            WHERE me.test_success IS true
        '''

        return pd.read_sql(query, engine)