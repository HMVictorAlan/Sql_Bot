import sqlite3
from itertools import chain

import openai
import pandas as pd
import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI
from langchain.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain.chains import create_sql_query_chain



import utils as utl
from views import options, configuration, inicio, contacto

# DB

st.set_page_config(layout="wide", page_title='Mysql Bot')
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()

def navigation():
    route = utl.get_current_route()
    if route == "inicio":
        inicio.load_view()
    elif route == "contacto":
        contacto.load_view()
    elif route == "options":
        options.load_view()
    elif route == "configuration":
        configuration.load_view()
    elif route == "chat":
        @st.cache_data()
        def load_data(url):

            df = pd.read_csv(url)
            return df

        def prepare_data(df):

            df.columns = [x.replace(' ', '_').lower() for x in df.columns]
            return df

        table_name = 'statesdb'
        uri = "file::memory:?cache=shared"

        st.markdown("<h1 style='text-align: center; color: #d4d4d4;'> ¿Qué duda tienes? </h1>", unsafe_allow_html=True)
        st.subheader('Sube tu archivo')

        # lear archivo
        uploaded_file = st.file_uploader("Elija un archivo csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df)

            # llave api
            openai_api_key = st.text_input(
                "Llave API",
                placeholder='1234567890',
                type='password',
                disabled=False,
                help='Ingrese su clave API de OpenAI.'
            )

            # query
            user_q = st.text_input(
                "Consulta de usuario",
                help="Ingrese una pregunta basada en el conjunto de datos.")


            # confirmar datos a sql
            data = prepare_data(df)
            conn = sqlite3.connect(uri)
            data.to_sql(table_name, conn, if_exists='replace', index=False)

            # crear base de datos
            eng = create_engine(
                url='sqlite:///file:memdb1?mode=memory&cache=shared',
                poolclass=StaticPool,  # conexión única para solicitudes
                creator=lambda: conn)
            db = SQLDatabase(engine=eng)

            # crear una conexión AI abierta y una cadena de base de datos
            if openai_api_key:
                llm = ChatOpenAI(
                    openai_api_key=openai_api_key,
                    temperature=0,  # escala creativa
                    max_tokens=300)
                db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
                chain = create_sql_query_chain(llm, db)

            # ejecutar consulta y mostrar sql query
            if openai_api_key and user_q:
                response = chain.invoke({"question": user_q})
                st.write(response)

            # ejecutar consulta y mostrar resultado
            if openai_api_key and user_q:
                result = db_chain.run(user_q)
                st.write(result)

    elif route == None:
        inicio.load_view()


navigation()
