import streamlit as st
import pandas as pd
import plotly.express as px


def _find_lat_lon_columns(df: pd.DataFrame):
    lat_candidates = [
        "Latitude",
        "latitude",
        "lat",
        "Lat",
        "lat_city",
    ]
    lon_candidates = [
        "Longitude",
        "longitude",
        "lon",
        "Lon",
        "lon_city",
    ]
    lat_col = next((c for c in lat_candidates if c in df.columns), None)
    lon_col = next((c for c in lon_candidates if c in df.columns), None)
    return lat_col, lon_col


def heat_map_body():
    st.write("# Pollution Heat Map")

    df = st.session_state.loaded_data

    # Select pollutant column from available AQI/Mean columns
    pollutant_cols = [
        c for c in df.columns if c.endswith(" AQI") or c.endswith(" Mean")
    ]
    pollutant_cols = sorted(pollutant_cols)
    if not pollutant_cols:
        st.warning(
            "No pollutant columns ending with ' AQI' or ' Mean' were found."
        )
        return

    selected = st.selectbox(
        "Select pollutant to visualize",
        pollutant_cols,
        help="Choose an AQI or Mean column",
    )

    lat_col, lon_col = _find_lat_lon_columns(df)
    if not lat_col or not lon_col:
        msg = (
            "No latitude/longitude columns found. Expected 'Latitude'/'Longitude' "
            "or 'lat_city'/'lon_city'."
        )
        st.warning(msg)
        return

    # Optional date filter (if present)
    date_col = "Date Local" if "Date Local" in df.columns else None
    if date_col is not None:
        try:
            dmin = pd.to_datetime(df[date_col]).min()
            dmax = pd.to_datetime(df[date_col]).max()
            with st.expander("Time filter"):
                start, end = st.date_input(
                    "Date range",
                    value=(dmin.date(), dmax.date()),
                    min_value=dmin.date(),
                    max_value=dmax.date(),
                )
            mask = (
                (pd.to_datetime(df[date_col]).dt.date >= start)
                & (pd.to_datetime(df[date_col]).dt.date <= end)
            )
            dfx = df.loc[mask].copy()
        except Exception:
            dfx = df.copy()
    else:
        dfx = df.copy()

    # Drop rows missing lat/lon/value
    dfx = dfx.dropna(subset=[lat_col, lon_col, selected]).copy()

    # Controls
    nbins = st.slider(
        "Spatial binning (higher = finer)",
        min_value=50,
        max_value=300,
        value=150,
        step=10,
    )
    agg = st.selectbox(
        "Aggregation",
        options=["mean", "median", "max"],
        help="How to aggregate within each spatial bin",
    )
    opacity = st.slider("Opacity", 0.1, 1.0, 0.85, 0.05)

    # Build density heatmap in lat/lon space (no Mapbox token required)
    histfunc = {"mean": "avg", "median": "median", "max": "max"}[agg]
    fig = px.density_heatmap(
        dfx,
        x=lon_col,
        y=lat_col,
        z=selected,
        nbinsx=nbins,
        nbinsy=nbins,
        histfunc=histfunc,
        color_continuous_scale="Turbo",
        labels={lon_col: "Longitude", lat_col: "Latitude", selected: selected},
    )
    fig.update_traces(hovertemplate="lon=%{x}<br>lat=%{y}<br>value=%{z}")
    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=30, b=0),
        title=f"Heat map of {selected}",
    )
    fig.update_traces(opacity=opacity)

    st.plotly_chart(fig, use_container_width=True)
