
from pathlib import Path
from random import randrange

from streamlit_tags import st_tags

import openai
from streamlit_option_menu import option_menu

import streamlit as st
import pandas as pd
from PIL import Image

def load_view():

	st.markdown('##')
	st.markdown("<h1 style='text-align: center; color: black;'> SQL BOT </h1>", unsafe_allow_html=True)
	st.markdown("<h2 style='text-align: center; color: grey'>La manera más rápida para resolver dudas SQL</h2>", unsafe_allow_html=True)

	col1, col2, col3 = st.columns([0.1, 0.2, 0.1])
	with col2:
		st.image("assets/images/giphy.gif")
	with col1:
		st.write(' ')
	with col3:
		st.write(' ')

	st.markdown("<h2 style='text-align: center; color: grey'> SQL BOT utiliza [ChatGpt], como su modelo de IA basada en chat de openAI y [LangChain] un marco para desarrollar aplicaciones basadas en modelos de lenguaje.</h2>", unsafe_allow_html=True)

	st.markdown(
		"<h2 style='text-align: center; color: grey'> La aplicación está diseñada para hacer que el proceso de análisis de datos de dificultad media a compleja sea más sencilla. En lugar de escribir consultas SQL usted mismo, la aplicación utiliza procesamiento de lenguaje natural para comprender su solicitud. Luego genera el SQL apropiado y lo ejecuta por usted.</h2>",
		unsafe_allow_html=True)

	









