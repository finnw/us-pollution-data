import streamlit as st
from app_pages.multi_page import MultiPage
import pandas as pd

from app_pages.time_series import time_series_body 
from app_pages.tree_map import tree_map_body 

app = MultiPage("US Pollution Dashboard")

app.add_page("Pollution Over Time", time_series_body)
app.add_page("Tree Map", tree_map_body)

# cache data for faster loading on page changes
@st.cache_data
def load_data():
    path = "./data/archive.zip"
    df = pd.read_csv(path, compression='zip', index_col=0)
    return df

# save data to session_state for use across app
# method from https://discuss.streamlit.io/t/is-there-a-way-to-get-data-cache-in-multi-page-app/55224/2
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = load_data()


app.run()