import streamlit as st
import pandas as pd
import plotly as px

def tree_map_body():
    st.write("# Tree Map")

    # cache data for faster loading on page changes
    @st.cache_data
    def load_your_data():
        path = "./data/archive.zip"
        df = pd.read_csv(path, compression='zip', index_col=0)
        return df

    df = load_your_data()

    # dictionary for mapping gas names to abbreviations
    # label function from https://discuss.streamlit.io/t/format-func-function-examples-please/11295/3
    gas_options = {'NO2':'Nitrous Oxides', 'O3':'Ozone', 'SO2':'Sulphur Oxide', 'CO':'Carbon Monoxide'}

    gas = st.selectbox(label='Select a gas', options=['NO2', 'O3', 'SO2', 'CO'], key="1", format_func=lambda x: gas_options.get(x))

    gas_aqi = gas + ' AQI'
    gas_mean = gas + ' Mean'

    st.write(f"Chart for {gas_options.get(gas)} AQI")
    import plotly.express as px
    fig = px.treemap(data_frame=df, path=['State','County'], values=gas_aqi, color=gas_mean, width=800,height=600, color_continuous_scale='turbid')
    st.plotly_chart(fig)
    st.write("---")