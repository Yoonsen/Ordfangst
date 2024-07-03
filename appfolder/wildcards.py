
import streamlit as st
import dhlab.api.dhlab_api as api
import dhlab as dh 
import pandas as pd
from PIL import Image
#import plotly.express as px


st.set_page_config(page_title="Wildcards", layout="wide", initial_sidebar_state="auto", menu_items=None)
st.session_state.update(st.session_state)

st.html(body = """
<style> body * {font-family:'DM Sans'}</style>
""")

# TODO: Add standard app header with logo + links + info
image = Image.open('DHlab_logo_web_en_black.png')
st.image(image, width = 200, )
#st.markdown('Les mer på [DHLAB-siden](https://nb.no/dh-lab/)')


word = st.text_input("Søkeord", placeholder="Angi søkeuttrykk med *", help="Sett * hvor som helst i ordet og så mange ganger det er passende. Pass bare på at et ord ikke kan ha * i både start og slutt. En av endene må ha et annet tegn")

with st.expander("Innstillinger"):
    freqlimcol, limcol = st.columns([1,1])
    

#factor = factorcol.number_input("Matchlengde", min_value=-10, value=2, help="Tallet som skrives inn her legges til lengden på ordet, målt i antall tegn inkludert * og bokstaver. Små tall vil typisk lage bøyningsparadigmer, mens store tall gir sammensetninger. Angivelsen kan også være negativ, men ikke mindre enn minus antall * i søkeuttrykket")

freqlim = freqlimcol.number_input("Laveste frekvensverdi",min_value=1, value=10)

limit = limcol.number_input("Resultatstørrelse", min_value=5, value=1000)

df = api.wildcard_search(word, factor=50, freq_limit=freqlim, limit=limit).reset_index(names=["words"])


data = df.sort_values(by="freq", ascending=False)
data["choice"] = False

data_col, viz_col = st.columns([2,2])


options = data_col.data_editor(
    data, 
    column_config={
        "choice": st.column_config.CheckboxColumn(
            "Valgt",
            help = "Velg ord du vil se trendlinjer for",
            #default=False,
        )
    },
#    disabled="freq",
    hide_index=True,
    
)

chosen = options[options.choice].words.tolist()

from_year, to_year = viz_col.select_slider("Årstall", options=list(range(1800, 2025, 1)), value=(1800, 2024))
lines = dh.Ngram(chosen, from_year=from_year, to_year=to_year).frame

viz_col.line_chart(lines)
