from io import BytesIO
import pandas as pd


# External stylesheet to get the icons
#style = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
style = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">'

## NB symbol
nb_logo_svg = """<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 350" width="60px" height="60px">
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
github_icon = """<a href="https://github.com/Yoonsen/Ordfangst" target="_blank" style="color: black; text-decoration: none; padding-left: 5px;">
    <i class="fab fa-github fa-1x" style="color: #262730;"></i>
</a>"""

email_icon = """<a href="https://www.nb.no/dh-lab/kontakt/" target="_blank" style="padding-left: 5px;">
    <i  class="fas" style="font-size:15px; color: #262730;">&#xf0e0;</i>
</a>
</div>
"""

dhlab_header_html =f"""<div style="display: inline-block; clear: both; padding-bottom:20px">
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
