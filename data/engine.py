import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

@st.cache_resource
def get_engine():

    db_conf = st.secrets['connections']['neon']

    connection_url = URL.create(
        drivername='postgresql+psycopg2',
        username=db_conf['username'],
        password=db_conf["password"],
        host=db_conf["host"],
        port=int(db_conf["port"]),
        database=db_conf["database"]
    )

    return create_engine(
                connection_url,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={
                    'sslmode': 'require',
                    'connect_timeout': 5,
                    'keepalives': 1,
                    'keepalives_idle': 30,
                    'keepalives_interval': 10,
                    'keepalives_count': 5
                }
    )