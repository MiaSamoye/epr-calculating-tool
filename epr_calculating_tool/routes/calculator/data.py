import streamlit as st
import pandas
from streamlit_gsheets import GSheetsConnection
ttl_seconds = 43200
sheet_connection = st.connection("gsheets", type=GSheetsConnection, ttl=ttl_seconds)


def get_industries():
    return sheet_connection.read(worksheet="list_of_industries")


def get_classifications(industry: str):
    classification_data = sheet_connection.read(worksheet="list_of_classifications")

    result = classification_data.loc[classification_data["industry_id"] == industry]

    return result
