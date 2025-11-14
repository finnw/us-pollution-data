
import streamlit as st
from app_pages.multi_page import MultiPage
import pandas as pd
from app_pages.intro import intro_body
from app_pages.heat_map import heat_map_body
from app_pages.time_series import time_series_body
from app_pages.tree_map import tree_map_body
from utils.population_join import (
    enrich_with_centroids,
    enrich_with_state_population,
    enrich_with_city_population,
)
from pathlib import Path
from app_pages.measurement_coverage import measurement_coverage_body
from app_pages.population_correlation import population_correlation_body
from app_pages.event_impact import event_impact_body
from app_pages.regional_differences import regional_differences_body

app = MultiPage("US Pollution Dashboard")

# Put Heat Map first so the app loads a robust page by default
# Load a light page first so initial render is fast
app.add_page("Introduction", intro_body)
app.add_page("Heat Map", heat_map_body)
app.add_page("Measurement Coverage", measurement_coverage_body)
app.add_page("Population & Pollution Correlation", population_correlation_body)
app.add_page("Pollution Over Time", time_series_body)
app.add_page("Tree Map", tree_map_body)
app.add_page("Event Impact Dashboard", event_impact_body)
app.add_page("Regional Differences", regional_differences_body)

# cache data for faster loading on page changes


@st.cache_data
def load_data():
    # Prefer pre-enriched Parquet, then CSV zip, then fallback to original
    pq_path = Path("./data/cleaned_enriched.parquet")
    csv_zip_path = Path("./data/cleaned_enriched.csv.zip")
    base_path = Path("./data/cleaned_pollution_data.zip")
    df = None
    if pq_path.exists():
        df = pd.read_parquet(pq_path)
    elif csv_zip_path.exists():
        df = pd.read_csv(csv_zip_path, compression='zip')
    elif base_path.exists():
        df = pd.read_csv(base_path, compression='zip', index_col=0)
        try:
            df = enrich_with_centroids(df)
            df = enrich_with_state_population(df)
            df = enrich_with_city_population(df)
        except Exception:
            pass
    else:
        st.error(
            "No suitable data file found. "
            "Please ensure a cleaned dataset is present."
        )
        return pd.DataFrame()
    return df

# save data to session_state for use across app
# Based on Streamlit community approach for caching across multi-page apps


if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = load_data()


app.run()
