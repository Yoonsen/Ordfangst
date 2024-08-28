
import pandas as pd
import streamlit as st
import dhlab.api.dhlab_api as api
import dhlab as dh
import utils


@st.cache_data
def to_excel(dfs):
    return utils.to_excel(*dfs)


@st.cache_data
def load_corpus(**kwargs):
    return dh.Corpus(**kwargs)


st.set_page_config(
    page_title="Ordfangst", layout="wide", initial_sidebar_state="auto", menu_items=None, page_icon=utils.nb_favicon,
)
st.session_state.update(st.session_state)

st.markdown(utils.style, unsafe_allow_html=True)
st.markdown(utils.dhlab_header_html, unsafe_allow_html=True)

st.title("Ordfangst")
st.subheader("Finn ord og sammenstillinger i NBs bokkorpus")

### Organiserer med kolonner
wordcol, _, expcol = st.columns([3, 1, 4])  # Krymper mellomrommet litt (ILD 18.07.2024)

with wordcol:
    word = st.text_input(
        "Søkeord",
        placeholder="Angi søkeuttrykk med * som jokertegn",
        help="Sett * hvor som helst i ordet, gjerne flere ganger. Eneste begrensning er * ikke kan være i både start og slutt",
    )


with expcol:
    st.write(" ")  # add some space on top of expander to align with wordcol
    with st.expander("Søkefilter"):      # separate settings for word search and data viewing 
        factorcol, freqlimcol, limcol = st.columns([1, 1, 1])

        ## har satt tilbake til kontekstgruppering - forskjellige grunner... LGJ 4. juli 2024 ###

        with factorcol:
            factor = st.number_input(
                "Matchlengde",
                min_value=-10,
                value=st.session_state.get("factor", 20),
                help=("Tallet som skrives inn her legges til lengden på ordet, målt i antall tegn inkludert * og bokstaver. "
                      "Små tall vil typisk lage bøyningsparadigmer, mens store tall gir sammensetninger. "
                      "Angivelsen kan også være negativ, men ikke mindre enn minus antall * i søkeuttrykket"
                      ),
                key="factor",
            )

        with freqlimcol:
            freqlim = st.number_input("Laveste frekvensverdi", min_value=1, value=10, help="Filtrer vekk ord med lavere frekvens enn dette")

        with limcol:
            limit = st.number_input("Resultatstørrelse", min_value=5, value=1000, help="Antall ord som skal hentes ut.")
            
        
        fromcol,tocol = st.columns([1, 1])
        # separate time period settings for word search from n-gram-viewing 
        with fromcol:
            #from_year = st.number_input("Fra år", min_value=1800, max_value=2024,value=1800, help="Første året i tidsperioden du vil søke i")
            pass 

        with tocol:    
            #to_year = st.number_input("Til år", min_value=1800, max_value=2024,value=2024, help="Siste året i tidsperioden du vil søke i")
            pass
        
        filnavn = st.text_input(
            "Filnavn for nedlasting", f"ordfangst_{word.strip('*') if word else 'søkeord'}.xlsx"
        )

     
# Perform wildcard search
df = api.wildcard_search(
    word, factor=st.session_state["factor"], freq_limit=freqlim, limit=limit
).reset_index(names=["ord"]).rename(columns={"freq": "frekvens"})
 
 
# Gather data results for multisheet-downloading
to_download = []
### Display results
if df.empty:
    st.write("") # Before searching, the data editor will not be displayed
else:
    data = df.sort_values(by="frekvens", ascending=False)    
    to_download.append(data.copy())
        
    st.write("") ## add space
    
    data_col, viz_col = st.columns([2, 2])

    ## ---- Organiserer kolonnene med kontekstgruppering --- LGJ: 4.7.2024 ###
    with data_col:
        st.subheader("Søketreff")
        data["choice"] = False
        options = st.data_editor(
            data,
            column_config={
                "choice": st.column_config.CheckboxColumn(
                    "valgt",
                    help="Velg ord du vil se trendlinjer for",
                    # default=False,
                )
            },
            #    disabled="freq",
            hide_index=True,
            use_container_width=True,
        )
        chosen = options[options.choice].ord.tolist()


    with viz_col:
        if chosen:
            st.subheader("Trendlinjer")
            
            mode_col,  year_col = st.columns([1,2 ])
            with mode_col:
                # LGJ: setter valgene i små bokstaver for at det skal virke med mode
                # kan beholde og gjøre x.lower() i stedet
                
                mode = st.radio("Frekvenstype", ["absolutt", "relativ"], index=0)

            with year_col:
                from_year, to_year = st.select_slider("Årstall", options=list(range(1800, 2025, 1)), value=(1800, 2024))
                
            # LGJ gjør nram for både avis og bok
            
            ngrams = pd.concat([dh.Ngram(chosen, from_year=from_year, to_year=to_year, mode=mode, doctype="bok").frame,dh.Ngram(chosen, from_year=from_year, to_year=to_year, mode=mode, doctype="avis").frame])
            ngrams = ngrams.groupby(ngrams.index).sum()
            
            st.line_chart(ngrams)
            
            trendlines = ngrams.copy()
            trendlines["Årstall"] = trendlines.index
            trendlines.reset_index(drop=True, inplace=True)
            to_download.append(trendlines[["Årstall"] + chosen])
 
        else:
            st.write("Velg ord i tabellen til venstre for å se trendlinjer")
    
    if chosen: 
        st.subheader("Konkordanser")
    

        word_query = " OR ".join(chosen)
        #st.write(f"Let etter dokumenter med {word_query}")

        ## LGJ: lar konk trigges av en knapp
        if st.button(f"Finn konkordanser for {word_query}"):
            try:
                _corpus = load_corpus(fulltext=word_query, from_year=from_year, to_year=to_year, limit="1000")
    
                _w_concs = []
                for w in chosen:
                    w_concs = dh.Concordance(corpus=_corpus, query=w, limit=5000)
                    _w_concs.append(w_concs.frame)
    
                _concs = pd.concat(_w_concs, axis=0)
        
                concs = utils.format_conc_table(_corpus.frame, _concs)
                to_download.append(concs.sort_values(by="Årstall"))
                
                st.dataframe(
                    concs,
                    column_config={
                        "URL": st.column_config.LinkColumn(
                            "nb.no",
                            help="Les i Nettbiblioteket",
                            display_text="🔗",
                            disabled=True,
                            width="small", 
                        ),
                      #  "Årstall": st.column_config.DateColumn(
                       #     "Årstall",
                       #     format="YYYY",
                        #    width="small",
                       # )
                    },
                    #disabled="urn",
                    hide_index=True,
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Kunne ikke hente konkordanser: {e}")


    
    full_download_button = data_col.download_button( # place right below the wordlist AFTER the results are ready

        ":arrow_down: Excel",
        to_excel(to_download), 
        filnavn, #f"ordfangst_{word.strip('*')}_{from_year}-{to_year}.xlsx", 
        help="Last ned data til en excel-fil"
    )
    
    if full_download_button:
        pass
