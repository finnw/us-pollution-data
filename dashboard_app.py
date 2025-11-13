import streamlit as st
from app_pages.multi_page import MultiPage

from app_pages.time_series import time_series_body 
from app_pages.tree_map import tree_map_body 

app = MultiPage("US Pollution Dashboard")

app.add_page("Pollution Over Time", time_series_body)
app.add_page("Tree Map", tree_map_body)

app.run()