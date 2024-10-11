import streamlit as st
import os
from epr_calculating_tool.config import BASE_DIR
from PIL import Image

PAGES_DIRECTORY = os.path.join(BASE_DIR, "routes")

im = Image.open("favicon.png")

st.set_page_config(
    page_title="AQUILA Welcome page",
    page_icon=im,
    layout="wide"
)

st.logo("aquila-logo.png", link=None, icon_image=None)

if "classification_costs" not in st.session_state:
    st.session_state.classification_costs = {}
if "transport_costs" not in st.session_state:
    st.session_state.transport_costs = {}
if "recycling_costs" not in st.session_state:
    st.session_state.recycling_costs = {}
    
home = st.Page(
    os.path.join(PAGES_DIRECTORY, "home", "page.py"),
    title="Welcome Page",
    icon=":material/home:",
    default=True,
)
calculator = st.Page(
    os.path.join(PAGES_DIRECTORY, "calculator", "page.py"),
    title="EPR Financial Contribution",
    icon=":material/calculate:",
    url_path="/calculator",
)

active_pages = [home, calculator]

pg = st.navigation(active_pages)

if __name__ == "__main__":
    pg.run()
