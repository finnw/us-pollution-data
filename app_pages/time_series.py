import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

    df_time = df_state.groupby(['year', 'pollutant'], sort=False)['aqi'].mean().reset_index()
    time_sel = 'year'

    # line chart for pollution over time
    # seaborn integration from https://docs.kanaries.net/topics/Streamlit/streamlit-seaborn
    st.write(f"Chart showing AQI by Pollutant over time")
    fig = sns.lineplot(data=df_time, x=time_sel, y='aqi', hue='pollutant')
    st.pyplot(fig.get_figure())
    st.write("---")
