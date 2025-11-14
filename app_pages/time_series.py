import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.express as px

def time_series_body():
    df = st.session_state.loaded_data

    st.write("## Pollution Over Time")

    # Only use AQI columns that exist in the DataFrame
    possible_aqi_cols = ['NO2 AQI', 'O3 AQI', 'SO2 AQI', 'CO AQI']
    available_aqi_cols = [col for col in possible_aqi_cols if col in df.columns]
    if not available_aqi_cols:
        st.error("No AQI columns found in the dataset.")
        return
    df_state = df.groupby(['State', 'Date Local'], sort=False)[available_aqi_cols].mean().reset_index()
    df_state = df_state.melt(id_vars=['State', 'Date Local'], value_vars=available_aqi_cols, var_name='pollutant', value_name='aqi')

    # group data by time values, default year
    # select for year + month, month mean, daily mean and day of week
    # convert Date Local to date format
    df_state['Date Local'] = pd.to_datetime(df_state['Date Local'])
    df_state.sort_values(by='Date Local', inplace=True)

    @st.cache_data
    def add_cols(df_state):
        # add datetime columns for charts
        df_state['year'] = df_state['Date Local'].dt.year
        df_state['year and month'] = df_state['Date Local'].dt.strftime('%Y %b')
        df_state['month'] = df_state['Date Local'].dt.month
        df_state['day of year'] = df_state['Date Local'].dt.dayofyear
        return df_state

    df_state = add_cols(df_state)

    # make list of states for filtering data
    state_list = df_state['State'].unique()
    state_list = np.insert(sorted(state_list), 0, 'ALL STATES')

    # make list of time selection types
    time_list = {'year': 'Change over time by year', 'year and month': 'Change over time by year and month', 'month': "Seasonality by month", 'day of year': 'Seasonality by day of year'}

    # select action based on chosen variables
    state_sel = st.selectbox(label='Choose a state', options=state_list, key="1")
    time_col = st.selectbox(label='Choose a time display type', options=time_list.keys(), key="2", format_func=lambda x: time_list.get(x))
   
    # set up columns to group by
    group_cols = ['pollutant']
    group_cols.append(time_col)

    # select specific state if required
    if state_sel == 'ALL STATES':
        df_time = df_state
    else:
        df_time = df_state.loc[df_state['State'] == state_sel]

    if time_col == 'month':
        df_time.sort_values(by='month', inplace=True)
    elif time_col == 'day of year':
        df_time.sort_values(by='day of year', inplace=True)
    else:
        df_time.sort_values(by='Date Local', inplace=True)

    # group data by selections
    df_time = df_time.groupby(group_cols, sort=False)['aqi'].mean().reset_index()

    # Defer heavy render until user clicks
    render = st.button("Load Chart")

    if not render:
        st.info("Adjust settings, then click 'Load Chart' to draw.")
        return
   
    # line chart for pollution over time
    # seaborn integration from https://docs.kanaries.net/topics/Streamlit/streamlit-seaborn
    st.write(f"Chart showing AQI by Pollutant over time")
    fig = px.line(df_time, x=time_col, y='aqi', color='pollutant')
    st.plotly_chart(fig)
    st.write("---")
