
import streamlit as st
import dhlab.api.dhlab_api as api
import dhlab as dh
import utils


@st.cache_data
def to_excel(df):
    return utils.to_excel(df)


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
 
 
### Display results

if df.empty:
    st.write("") # Before searching, the data editor will not be displayed
else:
    data = df.sort_values(by="frekvens", ascending=False)    

    ## append to container right below the search bar (wordcol) AFTER the results are ready
    download_button = wordcol.download_button(
        ":arrow_down: Excel", to_excel(data), filnavn, help="Last ned søketreffene til en excel-fil"
    )
    if download_button:
        pass
    
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
            
            mode_col,  year_col, button_col = st.columns([1,4, 1])
            with mode_col:
                mode = st.radio("Frekvenstype", ["Absolutt", "Relativ"], index=0)
                
            with year_col:
                from_year, to_year = st.select_slider("Årstall", options=list(range(1800, 2025, 1)), value=(1800, 2024))

            lines = dh.Ngram(chosen, from_year=from_year, to_year=to_year, mode=mode).frame
            
            st.line_chart(lines)
            
            with button_col:
                
                ngram_download_button = st.download_button( # place below the mode settings
                    ":arrow_down:",
                    to_excel(lines), 
                    f"ngram_{word.strip('*')}_{mode}_{from_year}-{to_year}.xlsx", 
                    help="Last ned data til en excel-fil"
                )
                
                if ngram_download_button:
                    pass

 
        else:
            st.write("Velg ord i tabellen til venstre for å se trendlinjer")
    
    if chosen: 
        st.subheader("Konkordanser")
    
        try:
            word_query = " OR ".join(chosen)
            _corpus = load_corpus(fulltext=word_query, from_year=from_year, to_year=to_year)
            _concs = dh.Concordance(corpus=_corpus, query=word_query)

            concs = utils.format_conc_table(_corpus, _concs)
            
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
                    "År": st.column_config.DateColumn(
                        "Publikasjonsår",
                        format="YYYY",
                        width="small",
                    )
                },
                #disabled="urn",
                hide_index=True,
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Kunne ikke hente konkordanser: {e}")
    
    
        

