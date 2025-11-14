import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.express as px

def time_series_body():
    df = st.session_state.loaded_data

    st.write("# Pollution Over Time")

    col_suffix = ' Mean'

    # group by state and day
    df_state = df.groupby(['State', 'Date Local'], sort=False)[['NO2 AQI', 'O3 AQI', 'SO2' + col_suffix, 'CO AQI']].mean().reset_index()

    # # method from https://stackoverflow.com/questions/44941082/plot-multiple-columns-of-pandas-dataframe-using-seaborn
    # # melt dataframe for AQIs
    df_state = df_state.melt(id_vars=['State', 'Date Local'], value_vars=['NO2 AQI', 'O3 AQI', 'SO2' + col_suffix, 'CO AQI'], var_name='pollutant', value_name='aqi')

    # group data by time values, default year
    # select for year + month, month mean, daily mean and day of week
    # convert Date Local to date format
    df_state['Date Local'] = pd.to_datetime(df_state['Date Local'])

    # # add year, month and day columns - TO BE REMOVED AFTER ETL UPDATE
    # df_state['year'] = df_state['Date Local'].dt.year
    # df_state['month'] = df_state['Date Local'].dt.month

    # make list of states for filtering data
    state_list = sorted(df_state['State'].unique())
    state_list = np.insert(state_list, 0, 'ALL STATES')

    # make list of time selection types
    time_list = {1: 'Change over time by year', 2: 'Change over time by year and month'}

    # select action based on chosen variables
    state_sel = st.selectbox(label='Choose a state', options=state_list, key="1")
    time_sel = st.selectbox(label='Choose a time display type', options=time_list.keys(), key="2", format_func=lambda x: time_list.get(x))
    group_cols = ['pollutant']

    # initialise time column with default value 'year'
    time_col = 'year'

    # cache df with new cols
    # check if col exists before adding

    # create df columns based on time selection
    def time_group(time_sel):
        match time_sel:
            case 1:
                time_col = 'year'
                df_state[time_col] = df_state['Date Local'].dt.year
            case 2:
                time_col = 'year and month'
                df_state[time_col] = df_state['Date Local'].dt.strftime('%b %Y')
        return time_col

    time_col = time_group(time_sel)
    group_cols.append(time_col)

    if state_sel == 'ALL STATES':
        df_time = df_state
    else:
        df_time = df_state.loc[df_state['State'] == state_sel]

    df_time = df_time.groupby(group_cols, sort=False)['aqi'].mean().reset_index()

    
    if st.button('Load Chart'):
        # line chart for pollution over time
        # seaborn integration from https://docs.kanaries.net/topics/Streamlit/streamlit-seaborn
        st.write(f"Chart showing AQI by Pollutant over time")
        fig = px.line(df_time, x=time_col, y='aqi', color='pollutant')
        st.plotly_chart(fig)
        st.write("---")
