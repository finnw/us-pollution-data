import streamlit as st
import pandas as pd
import plotly.express as px

def tree_map_body():
    st.write("# Tree Map")

    df = st.session_state.loaded_data

    # dictionary for mapping gas names to abbreviations
    # label function from https://discuss.streamlit.io/t/format-func-function-examples-please/11295/3
    gas_options = {'NO2':'Nitrous Oxides', 'O3':'Ozone', 'SO2':'Sulphur Oxide', 'CO':'Carbon Monoxide'}

    gas = st.selectbox(label='Select a gas', options=['NO2', 'O3', 'SO2', 'CO'], key="1", format_func=lambda x: gas_options.get(x))

    gas_aqi = gas + ' AQI'
    gas_mean = gas + ' Mean'

    df_chart = df.groupby(['State', 'County', 'City'], sort=False)[[gas_aqi, gas_mean]].mean().reset_index()

    st.write(f"Chart for {gas_options.get(gas)} AQI")
    fig = px.treemap(data_frame=df_chart, path=[px.Constant('United States'), 'State','County', 'City'], values=gas_aqi, color=gas_mean, maxdepth=2, 
                     width=800,height=600, color_continuous_scale='dense')
    st.plotly_chart(fig)
    st.write("---")