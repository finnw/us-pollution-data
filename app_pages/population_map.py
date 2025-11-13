import streamlit as st
import pandas as pd
import plotly.express as px


STATE_NAME_TO_ABBR = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

# Approximate land area (sq mi), public data (rounded), includes DC
STATE_LAND_AREA_SQMI = {
    'Alabama': 50745,
    'Alaska': 570641,
    'Arizona': 113594,
    'Arkansas': 52035,
    'California': 155779,
    'Colorado': 103642,
    'Connecticut': 4842,
    'Delaware': 1949,
    'District of Columbia': 61,
    'Florida': 53625,
    'Georgia': 57513,
    'Hawaii': 6423,
    'Idaho': 82643,
    'Illinois': 55519,
    'Indiana': 35826,
    'Iowa': 55857,
    'Kansas': 81823,
    'Kentucky': 39486,
    'Louisiana': 43566,
    'Maine': 30843,
    'Maryland': 9707,
    'Massachusetts': 7800,
    'Michigan': 56804,
    'Minnesota': 79627,
    'Mississippi': 46907,
    'Missouri': 68742,
    'Montana': 145546,
    'Nebraska': 76824,
    'Nevada': 109781,
    'New Hampshire': 8953,
    'New Jersey': 7354,
    'New Mexico': 121365,
    'New York': 47126,
    'North Carolina': 48618,
    'North Dakota': 69001,
    'Ohio': 40861,
    'Oklahoma': 68595,
    'Oregon': 95997,
    'Pennsylvania': 44743,
    'Rhode Island': 1034,
    'South Carolina': 30061,
    'South Dakota': 75811,
    'Tennessee': 41235,
    'Texas': 261232,
    'Utah': 82170,
    'Vermont': 9217,
    'Virginia': 39598,
    'Washington': 66456,
    'West Virginia': 24038,
    'Wisconsin': 54158,
    'Wyoming': 97093,
}


def population_map_body():
    st.write("# Population Map (Static Choropleth)")

    if 'loaded_data' not in st.session_state:
        st.info("Load data first to view the population map.")
        return

    df = st.session_state.loaded_data
    if 'population_state' not in df.columns:
        st.warning(
            "State population not found. I'll keep the page, but we need the "
            "population enrichment artifacts to render this choropleth."
        )
        return

    # Derive year values; filter to rows with population available
    if 'Date Local' not in df.columns:
        st.warning("Missing 'Date Local' column to select a year.")
        return

    dfx = df.copy()
    dfx['year'] = pd.to_datetime(dfx['Date Local']).dt.year
    dfx = dfx.dropna(subset=['population_state'])
    if dfx.empty:
        st.warning("No rows with state population available to plot.")
        return

    years = sorted(dfx['year'].unique())
    year = st.selectbox("Select year", options=years, index=len(years) - 1)
    metric = st.selectbox(
        "Metric",
        options=[
            "Population",
            "Population density (per sq mi)",
        ],
        help="Population is total count; density uses state land area.",
    )
    scale_mode = st.selectbox(
        "Color scaling",
        options=["Continuous", "Quantile bins"],
        help="Use quantile bins for more even color distribution.",
    )
    if scale_mode == "Quantile bins":
        n_bins = st.slider(
            "Number of bins",
            min_value=4,
            max_value=9,
            value=6,
            step=1,
        )

    # Aggregate to one row per state for the selected year
    plot_df = (
        dfx.loc[dfx['year'] == year]
        .groupby('State', as_index=False)['population_state']
        .max()
        .rename(columns={'population_state': 'Population'})
    )

    # Map to state abbreviations for Plotly USA choropleth mode
    plot_df['abbr'] = plot_df['State'].map(STATE_NAME_TO_ABBR)
    plot_df = plot_df.dropna(subset=['abbr'])

    if metric != "Population":
        plot_df['area_sqmi'] = plot_df['State'].map(STATE_LAND_AREA_SQMI)
        plot_df['Density'] = plot_df['Population'] / plot_df['area_sqmi']
    
    if plot_df.empty:
        st.warning("No state-level data to display for the selected year.")
        return

    color_col = 'Population' if metric == 'Population' else 'Density'
    hover = {'State': True, 'abbr': False}
    if 'Population' in plot_df.columns:
        hover['Population'] = ':.0f'
    if 'Density' in plot_df.columns and metric != 'Population':
        hover['Density'] = ':.1f'

    if scale_mode == "Quantile bins":
        series = plot_df[color_col].astype(float)
        # Use qcut to generate quantile-based bins; drop duplicate edges
        try:
            bins = pd.qcut(series, q=n_bins, duplicates='drop')
        except Exception:
            # Fallback: fewer bins if distribution is degenerate
            bins = pd.qcut(series, q=max(3, n_bins - 1), duplicates='drop')
        plot_df['bin'] = bins
        # Prepare a limited sequential palette matching bin count
        palette = px.colors.sequential.Viridis
        k = min(len(palette), plot_df['bin'].cat.categories.size)
        palette = palette[:k]
        fig = px.choropleth(
            plot_df,
            locations='abbr',
            locationmode='USA-states',
            color='bin',
            color_discrete_sequence=palette,
            scope='usa',
            hover_data=hover,
        )
        # Build legend caption with quantile breakpoints
        qs = [i / k for i in range(k + 1)] if k else []
        try:
            edges = series.quantile(qs).tolist() if qs else []
        except Exception:
            edges = []
        
        def _fmt(v: float) -> str:
            if metric == 'Population':
                try:
                    return f"{int(round(v)):,}"
                except Exception:
                    return str(v)
            try:
                return f"{v:,.1f}"
            except Exception:
                return str(v)
        if edges and len(edges) >= 2:
            items = []
            for i in range(len(edges) - 1):
                left = _fmt(edges[i])
                right = _fmt(edges[i + 1])
                items.append(f"Q{i+1}: {left} – {right}")
            st.caption(
                "Quantile bins (lower→higher): " + ", ".join(items)
            )
    else:
        fig = px.choropleth(
            plot_df,
            locations='abbr',
            locationmode='USA-states',
            color=color_col,
            color_continuous_scale='Viridis',
            scope='usa',
            hover_data=hover,
        )
    title_metric = (
        'Population' if metric == 'Population' else 'Population Density'
    )
    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=30, b=0),
        title=f"State {title_metric} — {year}",
    )
    st.plotly_chart(fig, use_container_width=True)

    if metric == 'Population':
        st.caption(
            "Tip: Switch to 'Population density (per sq mi)' to normalize "
            "by state land area."
        )
