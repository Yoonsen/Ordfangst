from io import BytesIO
import pandas as pd


# External stylesheet to get the icons
#style = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
style = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">'

## NB symbol
nb_favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" height="24" width="24" class="t2-icon t2-icon-logo" aria-hidden="true" focusable="false"><path fill="#ffffff" d="M 4.9 7.8 C 5.5 7.8 6 7.3 6 6.7 C 6 6.1 5.5 5.7 4.9 5.7 C 4.3 5.7 3.8 6.2 3.8 6.8 C 3.8 7.3 4.3 7.8 4.9 7.8 Z M 15.7 23.7 C 16.3 23.7 16.8 23.2 16.8 22.6 C 16.8 22 16.3 21.5 15.7 21.5 C 15.1 21.5 14.6 22 14.6 22.6 C 14.6 23.3 15.1 23.7 15.7 23.7 Z M 7.6 0.3 L 7.6 20.1 L 20.2 20.1 L 20.2 0.3 L 7.6 0.3 Z M 10.3 7.8 C 9.7 7.8 9.2 7.3 9.2 6.7 C 9.2 6.1 9.7 5.6 10.3 5.6 C 10.9 5.6 11.4 6.1 11.4 6.7 C 11.4 7.3 10.9 7.8 10.3 7.8 Z M 15.6 18.4 C 15 18.4 14.5 17.9 14.5 17.3 C 14.5 16.7 15 16.2 15.6 16.2 C 16.2 16.2 16.7 16.7 16.7 17.3 C 16.7 17.9 16.2 18.4 15.6 18.4 Z M 15.6 13.1 C 15 13.1 14.5 12.6 14.5 12 C 14.5 11.4 15 10.9 15.6 10.9 C 16.2 10.9 16.7 11.4 16.7 12 C 16.7 12.6 16.2 13.1 15.6 13.1 Z M 15.6 7.8 C 15 7.8 14.5 7.3 14.5 6.7 C 14.5 6.1 15 5.6 15.6 5.6 C 16.2 5.6 16.7 6.1 16.7 6.7 C 16.7 7.3 16.2 7.8 15.6 7.8 Z"></path></svg>"""

nb_logo_svg = """<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 325 350" width="60px" height="60px">
    <path d="m96.29,163.63c6.79,0,12.29-5.51,12.29-12.29s-5.5-12.29-12.29-12.29-12.29,5.51-12.29,12.29,5.5,12.29,12.29,12.29Z"/>
    <path d="m220.13,346.62c6.79,0,12.29-5.51,12.29-12.29s-5.5-12.29-12.29-12.29-12.29,5.51-12.29,12.29,5.5,12.29,12.29,12.29Z"/>
    <path d="m127.41,77v227.61h144.34V77H127.41Zm30.61,86.63c-6.79,0-12.29-5.51-12.29-12.29s5.5-12.29,12.29-12.29,12.29,5.51,12.29,12.29-5.5,12.29-12.29,12.29Zm61.21,121.58c-6.79,0-12.29-5.51-12.29-12.29s5.5-12.29,12.29-12.29,12.29,5.51,12.29,12.29-5.5,12.29-12.29,12.29Zm0-60.6c-6.79,0-12.29-5.51-12.29-12.29s5.5-12.29,12.29-12.29,12.29,5.51,12.29,12.29-5.5,12.29-12.29,12.29Zm0-60.98c-6.79,0-12.29-5.51-12.29-12.29s5.5-12.29,12.29-12.29,12.29,5.51,12.29,12.29-5.5,12.29-12.29,12.29Z"/>
</svg>"""

### symbol + name
nb_logo_html = f"""
<a href="https://nb.no/dhlab/"  style="color: black; text-decoration: none; padding-right: 15px;">
  <div style="display: inline-block; vertical-align: bottom;">{nb_logo_svg}</div>
  <span style="display: inline-block; vertical-align: bottom; font-size:20px;font-family:DM Sans;"><b>Nasjonalbiblioteket</b></span>
</a>
"""

### Icons
repo_link = "https://github.com/Yoonsen/Ordfangst"

github_icon = f"""<a href="{repo_link}" target="_blank" style="color: black; text-decoration: none; padding-left: 5px;">
<i class="fab fa-github fa-1x"></i>
</a>"""

email_icon = """<a href="https://www.nb.no/dh-lab/kontakt/" target="_blank" style="color: black; padding-left: 5px;">
<i class="fas" style="font-size:15px;">&#xf0e0;</i>
</a>
</div>
"""

dhlab_header_html =f"""<div style="display: inline-block; clear: both; padding-bottom:20px; opacity:0.75;">
{nb_logo_html}
{github_icon}
{email_icon}
</div>"""



def to_excel(df):
    """Make an excel object out of a dataframe as an IO-object"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    processed_data = output.getvalue()
    return processed_data

def format_concordances(conc_series):
    concs = conc_series.apply(split_bold_text)
    return pd.DataFrame(concs.tolist(), columns=["Før", "Ord", "Etter"])    

def split_bold_text(text):
    return [z for y in text.split("<b>") for z in y.split("</b>")]

def extract_html_link(link_text):
    return link_text.split("href = '")[1].split("'")[0]

def format_conc_table(corpus, concs):
    concs_meta = concs.frame.merge(corpus.frame, on="urn", how="left")
    
    contexts = concs_meta.concordance.apply(split_bold_text).tolist()
    multicol = pd.DataFrame(contexts, columns=["Før", "Ord", "Etter"])
    
    multicol["URL"] = concs_meta.link.apply(extract_html_link)

    multicol["Tittel"] = concs_meta.title                
    multicol["Forfatter"] = concs_meta.authors
    multicol["År"] = concs_meta.year
    multicol["Dokument-type"] = concs_meta.doctype
    return multicol
    