import streamlit as st
from app_pages.multi_page import MultiPage
import pandas as pd

from app_pages.heat_map import heat_map_body
from app_pages.time_series import time_series_body
from app_pages.tree_map import tree_map_body

app = MultiPage("US Pollution Dashboard")

# Put Heat Map first so the app loads a robust page by default
app.add_page("Heat Map", heat_map_body)
app.add_page("Pollution Over Time", time_series_body)
app.add_page("Tree Map", tree_map_body)

# cache data for faster loading on page changes


@st.cache_data
def load_data():
    path = "./data/cleaned_pollution_data.zip"
    df = pd.read_csv(path, compression='zip', index_col=0)
    return df

# save data to session_state for use across app
# Based on Streamlit community approach for caching across multi-page apps


if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = load_data()


app.run()
