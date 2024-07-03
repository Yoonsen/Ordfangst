
import streamlit as st
import dhlab.api.dhlab_api as api
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Wildcards", layout="wide", initial_sidebar_state="auto", menu_items=None)
st.session_state.update(st.session_state)

image = Image.open('DHlab_logo_web_en_black.png')
st.image(image, width = 200)
st.markdown('Les mer på [DHLAB-siden](https://nb.no/dh-lab/)')

wordcol, factorcol, freqlimcol, limcol = st.columns([2, 1, 1, 1])

with wordcol:
    word = st.text_input("Angi søkeuttrykk med *", "", help="Sett * hvor som helst i ordet og så mange ganger det er passende. Pass baer på at et ord ikke kan ha * i både start og slutt. En av endene må ha et annet tegn")

with factorcol:
    factor = st.number_input("Matchlengde", min_value=-10, value=2, help="Tallet som skrives inn her legges til lengden på ordet, målt i antall tegn inkludert * og bokstaver. Små tall vil typisk lage bøyningsparadigmer, mens store tall gir sammensetninger. Angivelsen kan også være negativ, men ikke mindre enn minus antall * i søkeuttrykket")

with freqlimcol:
    freqlim = st.number_input("Laveste frekvensverdi",min_value=1, value=10)
with limcol:
    limit = st.number_input("Resultatstørrelse", min_value=5, value=50)

df = api.wildcard_search(word, factor=factor, freq_limit=freqlim, limit=limit)

st.dataframe(df.sort_values(by="freq", ascending=False), use_container_width=True)
