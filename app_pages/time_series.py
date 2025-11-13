import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def time_series_body():
    df = st.session_state.loaded_data

    st.write("# Pollution Over Time")

    # group by state and day
    df_state = df.groupby(['State', 'Date Local'], sort=False)[['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']].mean().reset_index()

    # # method from https://stackoverflow.com/questions/44941082/plot-multiple-columns-of-pandas-dataframe-using-seaborn
    # # melt dataframe for AQIs
    df_state = df_state.melt(id_vars=['State', 'Date Local'], value_vars=['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI'], var_name='pollutant', value_name='aqi')

    # group data by time values, default year
    # select for year + month, month mean, daily mean and day of week
    # convert Date Local to date format
    df_state['Date Local'] = pd.to_datetime(df_state['Date Local'])

    # add year, month and day columns - TO BE REMOVED AFTER ETL UPDATE
    df_state['year'] = df_state['Date Local'].dt.year
    df_state['month'] = df_state['Date Local'].dt.month

    state_list = sorted(df_state['State'].unique())
    state_list = np.insert(state_list, 0, 'ALL STATES')

    # add slider to pick time frame?

    # select action based on chosen variables
    state_sel = st.selectbox(label='Choose a state', options=state_list, key="1")
    time_sel = 'year'

    if state_sel == 'ALL STATES':
        df_time = df_state.groupby(['year', 'pollutant'], sort=False)['aqi'].mean().reset_index()
    else:
        df_time = df_state.loc[df_state['State'] == state_sel]
        df_time = df_time.groupby(['year', 'pollutant'], sort=False)['aqi'].mean().reset_index()

    # df_time = df_state.groupby(['year', 'month', 'pollutant'], sort=False)['aqi'].mean().reset_index()
    
    if st.button('Load Chart'):
        # line chart for pollution over time
        # seaborn integration from https://docs.kanaries.net/topics/Streamlit/streamlit-seaborn
        st.write(f"Chart showing AQI by Pollutant over time")
        fig = px.line(df_time, x=time_sel, y='aqi', color='pollutant')
        st.plotly_chart(fig)
        st.write("---")
