import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def population_correlation_body():
    st.title('Population and Pollution Correlation')
    st.header('Hypothesis')
    st.write('This page explores whether areas with higher total population tend to have higher pollution levels. The analysis uses scatter plots to visualize pollutant values against total population.')
    st.markdown('---')

    df = st.session_state.loaded_data.copy()
    pop_col = None
    if 'Population' in df.columns:
        pop_col = 'Population'
    elif 'population_city' in df.columns:
        pop_col = 'population_city'
    elif 'population_state' in df.columns:
        pop_col = 'population_state'
    else:
        st.error('No population column found in dataset.')
        return
    df = df[df[pop_col].notnull()]
    pollutants = [c for c in df.columns if c.endswith(' AQI') or c.endswith(' Mean')]
    if not pollutants:
        st.warning('No pollutant columns found in the dataset.')
    else:
        st.write('### Pollutant vs Population Scatter Plots')
        fig, ax = plt.subplots()
        plotted = False
        for pollutant in pollutants:
            if pollutant in df.columns:
                valid = df[pop_col].notnull() & df[pollutant].notnull()
                if valid.any():
                    ax.scatter(df.loc[valid, pop_col], df.loc[valid, pollutant], alpha=0.3, label=pollutant)
                    plotted = True
        ax.set_xlabel('Population')
        ax.set_ylabel('Pollutant Value')
        ax.set_title('Pollutant vs Population')
        if plotted:
            ax.legend()
            st.pyplot(fig, use_container_width=True)
        else:
            st.warning('No valid data to plot for any pollutant.')
    st.markdown('---')
    st.header('Findings & Commentary')
    st.write('Review the scatter plots above to assess whether higher total population is associated with increased pollutant values. In this dataset, pollutant values sometimes appear higher in less populated areas. This could be due to local sources, monitoring site placement, travel patterns, or other regional factors. Further investigation is needed to clarify these relationships.')
