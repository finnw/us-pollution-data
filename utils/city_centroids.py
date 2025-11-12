from __future__ import annotations

from pathlib import Path
from typing import Dict, Mapping

import pandas as pd

# Public normalization helpers
_DEF_SUFFIXES = [
    " County", " county", " Parish", " parish", " Borough", " borough",
    " Census Area", " census area", " Municipality", " municipality",
    " City and Borough", " city and borough",
]

def normalize_city(value: str) -> str:
    return str(value).strip().lower()

def normalize_county(value: str) -> str:
    s = str(value).strip()
    for suf in _DEF_SUFFIXES:
        if s.endswith(suf):
            s = s[:-len(suf)]
            break
    return s

# Type alias for the nested centroid mapping
CentroidsDict = Dict[str, Dict[str, Dict[str, Dict[str, float]]]]


# IO

def load_centroids_json(path: str | Path) -> CentroidsDict:
    """
    Load nested centroids JSON (state -> county -> city -> {lat, lon}).
    Returns a plain Python dict with string keys and float values.
    """
    p = Path(path)
    import json
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Application


def apply_city_centroids(
    df: pd.DataFrame,
    centroids: Mapping[str, Mapping[str, Mapping[str, Mapping[str, float]]]],
    *,
    state_col: str = "State",
    county_col: str = "County",
    city_col: str = "City",
    lat_col: str = "lat_city",
    lon_col: str = "lon_city",
    source_col: str = "coord_source_city",
) -> pd.DataFrame:
    """
    Non-destructively apply city-centroid coordinates to a DataFrame using a
    nested dict: state -> normalized county (no suffix) -> lowercased city ->
    {lat, lon}.

    - Adds/overwrites lat_col, lon_col, source_col only for matched rows.
    - Returns the same DataFrame instance for convenience.
    """
    missing = [
        c for c in (state_col, county_col, city_col) if c not in df.columns
    ]
    if missing:
        raise KeyError(f"Missing expected columns: {missing}")

    # Ensure target columns exist
    for col in (lat_col, lon_col, source_col):
        if col not in df.columns:
            df[col] = None

    def _lookup(row):
        st = str(row[state_col]).strip()
        co = normalize_county(row[county_col]).strip().lower()
        ci = normalize_city(row[city_col])
        try:
            city_info = centroids[st][co][ci]
            return float(city_info.get("lat")), float(city_info.get("lon"))
        except Exception:
            return None

    mask = df[[state_col, county_col, city_col]].notna().all(axis=1)
    latlon = df.loc[mask, [state_col, county_col, city_col]].apply(
        _lookup, axis=1
    )

    hit_mask = latlon.notna()
    if hit_mask.any():
        hits = df.loc[mask].loc[hit_mask]
        hits = hits.assign(_latlon=latlon.loc[hit_mask].values)
        df.loc[hits.index, lat_col] = hits["_latlon"].map(lambda t: t[0])
        df.loc[hits.index, lon_col] = hits["_latlon"].map(lambda t: t[1])
        df.loc[hits.index, source_col] = "city_county_state"

    return df
