from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

st.set_page_config(
    page_title="Streamlit Modular Template",
    layout="wide",
)

_assets = Path(__file__).parent / "assets"
st.logo(str(_assets / "logo.png"), icon_image=str(_assets / "logo_sm.svg"))

menu = {
    "Info": [
        st.Page("pages/home.py", title="Readme", icon=":material/description:"),
    ],
    "Demo": [
        st.Page("pages/example.py", title="Example", icon=":material/widgets:"),
        st.Page("pages/product.py", title="Product", icon=":material/info:"),
        st.Page("pages/form.py", title="Form", icon=":material/edit_note:"),
    ],
}

st.markdown(
    """<style>
    hr { margin-top: 0.25rem !important; margin-bottom: 0.25rem !important; }
    [data-testid="stMarkdownContainer"] p { margin: 0 !important; }
    </style>""",
    unsafe_allow_html=True,
)

pg = st.navigation(menu)
pg.run()
