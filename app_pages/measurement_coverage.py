import streamlit as st
import pandas as pd
import plotly.express as px

def measurement_coverage_body():
    st.title('Measurement Coverage Bias')
    st.header('Hypothesis')
    st.write('Pollution monitoring sites are clustered in cities, potentially underrepresenting rural pollution.')
    st.write('This page visualizes the locations of monitoring sites and their associated city populations to assess coverage bias.')
    st.markdown('---')

    df = st.session_state.loaded_data.copy()
    plot_df = df.dropna(subset=['lat_city', 'lon_city', 'population_city'])
    plot_df = plot_df[plot_df['population_city'] > 0]
    fig = px.scatter_mapbox(
        plot_df,
        lat='lat_city',
        lon='lon_city',
        color='population_city',
        size='population_city',
        mapbox_style='carto-positron',
        zoom=3,
        title='Monitoring Site Coverage'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('---')

    st.header('Findings & Commentary')
    st.write('- Most monitoring sites are located in cities with higher populations (larger, darker circles).')
    st.write('- Rural or less populated areas have fewer or no monitoring sites, indicating sparse coverage.')
    st.write('- This supports the hypothesis: monitoring coverage is biased toward urban centers, which may lead to underrepresentation of rural pollution in the dataset.')
    st.write('- For more robust conclusions, further analysis could compare pollutant levels in covered vs. uncovered areas, or examine the impact of coverage bias on reported air quality trends.')
