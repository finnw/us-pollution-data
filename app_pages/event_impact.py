import streamlit as st
import pandas as pd
import plotly.express as px

def event_impact_body():
    df = st.session_state.loaded_data.copy()
    df['Date Local'] = pd.to_datetime(df['Date Local'])
    df['year'] = df['Date Local'].dt.year
    pollutants = [c for c in df.columns if c.endswith(' AQI') or c.endswith(' Mean')]

    EVENTS = {
        'Hurricane Sandy (2012, NY/NJ)': {
            'states': ['New York', 'New Jersey'],
            'year_range': (2010, 2014),
            'event_year': 2012,
            'color': 'red',
            'label': 'Hurricane Sandy'
        },
        'Clean Power Plan (2015, WV/OH/KY)': {
            'states': ['West Virginia', 'Ohio', 'Kentucky'],
            'year_range': (2012, 2016),
            'event_year': 2015,
            'color': 'blue',
            'label': 'Clean Power Plan'
        }
    }

    st.title('Event Impact on US Pollution')
    st.header('Hypothesis')
    st.write('Major events within the dataset range (e.g., Hurricane Sandy in 2012, Clean Power Plan in 2015) cause observable changes in pollutant levels over time.')
    st.markdown('---')

    st.subheader('Select Chart')
    chart_options = ['US Yearly Pollutant Trends (Default)'] + list(EVENTS.keys())
    chart_choice = st.selectbox('Choose chart to display:', chart_options, index=0)

    if chart_choice == 'US Yearly Pollutant Trends (Default)':
        fig = px.line()
        for pollutant in pollutants:
            yearly = df.groupby('year')[pollutant].mean()
            fig.add_scatter(x=yearly.index, y=yearly.values, mode='lines', name=pollutant)
        fig.update_layout(title='Yearly Pollutant Trends (Event Impact)', xaxis_title='Year', yaxis_title='Mean Pollutant Value')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('---')
        st.header('Findings & Conclusion')
        st.write('This chart shows overall yearly pollutant trends for the US. Select an event for focused analysis and findings.')
    else:
        event = EVENTS[chart_choice]
        states = event['states']
        year_min, year_max = event['year_range']
        event_year = event['event_year']
        color = event['color']
        label = event['label']
        dff = df[df['State'].isin(states) & (df['year'] >= year_min) & (df['year'] <= year_max)]
        fig = px.line()
        for pollutant in pollutants:
            yearly = dff.groupby('year')[pollutant].mean()
            fig.add_scatter(x=yearly.index, y=yearly.values, mode='lines', name=pollutant)
        fig.add_vline(x=event_year, line_dash='dash', line_color=color)
        fig.add_annotation(x=event_year+0.1, y=max([dff.groupby('year')[p].mean().max() for p in pollutants]),
                            text=label, showarrow=False, font=dict(color=color), yanchor='top', textangle=-90)
        fig.update_layout(title=f"Pollutant Trends: {label}", xaxis_title='Year', yaxis_title='Mean Pollutant Value')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('---')
        st.header('Findings & Conclusion')
        if chart_choice.startswith('Hurricane Sandy'):
            st.write('In 2012 (Hurricane Sandy), O3 AQI, NO2 AQI, and NO2 Mean show an increase from 2011 to 2012, followed by a decline in 2013. This pattern suggests a possible event-driven impact and subsequent recovery.')
        else:
            st.write('In 2015 (Clean Power Plan), the effect appears delayed, with pollutant levels showing more noticeable changes in 2016 rather than immediately in 2015.')
