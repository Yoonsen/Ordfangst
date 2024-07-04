
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

wordcol, _,  expcol = st.columns([2, 1, 2])

with wordcol:
    word = st.text_input("Søkeord", placeholder="Angi søkeuttrykk med * som jokertegn", help="Sett * hvor som helst i ordet, gjerne flere ganger. Eneste begrensning er * ikke kan være i både start og slutt")

with expcol:
    st.write(' ') # add some space on top of expander to align with wordcol
    with st.expander("Innstillinger"):
        
        factorcol, freqlimcol, limcol = st.columns([1,1,1])
        
        with factorcol:
            factor = st.number_input("Matchlengde", min_value=-10, value=st.session_state.get('factor',20), help="Tallet som skrives inn her legges til lengden på ordet, målt i antall tegn inkludert * og bokstaver. Små tall vil typisk lage bøyningsparadigmer, mens store tall gir sammensetninger. Angivelsen kan også være negativ, men ikke mindre enn minus antall * i søkeuttrykket", key="factor")
        
        with freqlimcol:
            freqlim = st.number_input("Laveste frekvensverdi",min_value=1, value=10)
        
        with limcol:
            limit = st.number_input("Resultatstørrelse", min_value=5, value=1000)


df = api.wildcard_search(word, factor=st.session_state['factor'], freq_limit=freqlim, limit=limit).reset_index(names=["words"])
data = df.sort_values(by="freq", ascending=False)
data["choice"] = False

## add space
st.write(' ')
st.write(' ')

## Columns for slider and ngram

data_col, year_col = st.columns([2,2])

with data_col:
    options = st.data_editor(
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

with year_col:
    from_year, to_year = st.select_slider("Årstall", options=list(range(1800, 2025, 1)), value=(1800, 2024))
    st.write('---')
    lines = dh.Ngram(chosen, from_year=from_year, to_year=to_year).frame
    st.line_chart(lines)
