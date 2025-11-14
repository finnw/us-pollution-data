import streamlit as st
import pandas as pd
import plotly.express as px

def regional_differences_body():
    st.title('Regional Pollution Differences')
    st.header('Hypothesis')
    st.write('Pollution levels vary significantly between different regions of the United States due to factors such as geography, climate, and local sources.')
    st.markdown('---')

    df = st.session_state.loaded_data.copy()
    region_col = None
    for col in ['region', 'Region', 'us_region', 'state_region']:
        if col in df.columns:
            region_col = col
            break
    if not region_col:
        st.error('No region column found in dataset.')
        return
    pollutants = [c for c in df.columns if c.endswith(' AQI') or c.endswith(' Mean')]
    if not pollutants:
        st.warning('No pollutant columns found in the dataset.')
        return
    selected_pollutant = st.selectbox('Select pollutant to compare by region:', pollutants)
    plot_df = df.dropna(subset=[region_col, selected_pollutant])
    # Remove rows with invalid region values
    plot_df = plot_df[plot_df[region_col].notnull() & (plot_df[region_col] != '')]
    # Sample if dataset is large
    max_rows = 2000
    if len(plot_df) > max_rows:
        plot_df = plot_df.sample(n=max_rows, random_state=42)
    if plot_df.empty:
        st.warning('No valid data to plot for the selected pollutant and region.')
        return
    fig = px.box(plot_df, x=region_col, y=selected_pollutant, points='all', title=f'{selected_pollutant} by Region')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('---')
    st.header('Findings & Commentary')
    st.markdown('''
**How to interpret the chart:**
- Each boxplot shows the distribution of pollutant values for a US region (West, Northeast, Midwest, South, Other).
- The box represents the median and quartiles; dots show individual data points and outliers.
- Higher boxes mean higher pollution levels in that region.
- The "Other" region includes records not matched to a standard US region (e.g., non-US states or unrecognized names).
- Compare boxes to see which regions have more pollution or variability.
''')
    st.write('Differences may reflect local sources, climate, or policy impacts.')
