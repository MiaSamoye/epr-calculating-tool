import streamlit as st
from epr_calculating_tool.config import BASE_DIR
import os


with open(os.path.join(BASE_DIR, "routes", "home", "home.md")) as home_md:
    st.markdown(home_md.read())

st.logo("aquila-logo.png", link=None, icon_image=None)