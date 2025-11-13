import streamlit as st

def time_series_body():
    df = st.session_state.loaded_data

    st.write("This is page 1")
    st.write(df.head())
