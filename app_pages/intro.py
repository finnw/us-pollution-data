import streamlit as st

def intro_body():
    st.write("## 🌍 Welcome to the Pollution Insights Dashboard")
    st.write("This interactive Streamlit app helps you explore and understand pollution trends across the United States through clear, engaging visualizations.\
             Whether you’re interested in geographic patterns, historical changes, or regional breakdowns, the app provides intuitive tools to uncover meaningful insights.")
    st.write('### 📑 Pages Overview')
    st.write('* **Heat Map** - 🗺️ Visualizes pollution levels across the United States on an interactive map, making it easy to spot geographic hotspots and regional differences.')
    st.write('* **Pollution Over Time** - ⏳ Tracks pollution trends over time, allowing you to observe changes, identify patterns, and analyze long-term environmental shifts.')
    st.write('* **Tree Map** - 🌳 Breaks down pollution levels by region in a hierarchical tree map, offering a clear view of how different areas contribute to overall pollution.')
    st.write('* **Measurement Coverage** - 🗺️ Visualizes coverage bias with a map showing monitoring locations alongside population distribution, helping identify gaps in measurement.')
    st.write('* **Population and Pollution Correlation** - 📊 Displays a scatterplot illustrating the relationship between pollutant levels and population size, revealing potential exposure risks.')
    st.write('* **Event Impact Dashboard** - 📈 Provides a line graph of pollutant levels over time with markers for major events, enabling analysis of environmental and policy impacts.')
    st.write('* **Regional Differences** - 📦 Uses boxplots to compare pollutant distributions across U.S. regions (West, South, Northeast, Midwest), highlighting variability and disparities.')
    st.write('### 🚀 How to Navigate')
    st.write('Use the sidebar to switch between pages.')
    st.write('Each visualization is interactive, so you can zoom, filter, and explore the data in detail.')
    st.write('Designed to be both informative for researchers and accessible for anyone curious about environmental data.')