from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from .city_centroids import (
    apply_city_centroids,
    load_centroids_json,
    normalize_city,
)


STATE_NAME_TO_FIPS: Dict[str, str] = {
    'Alabama': '01',
    'Alaska': '02',
    'Arizona': '04',
    'Arkansas': '05',
    'California': '06',
    'Colorado': '08',
    'Connecticut': '09',
    'Delaware': '10',
    'District of Columbia': '11',
    'Florida': '12',
    'Georgia': '13',
    'Hawaii': '15',
    'Idaho': '16',
    'Illinois': '17',
    'Indiana': '18',
    'Iowa': '19',
    'Kansas': '20',
    'Kentucky': '21',
    'Louisiana': '22',
    'Maine': '23',
    'Maryland': '24',
    'Massachusetts': '25',
    'Michigan': '26',
    'Minnesota': '27',
    'Mississippi': '28',
    'Missouri': '29',
    'Montana': '30',
    'Nebraska': '31',
    'Nevada': '32',
    'New Hampshire': '33',
    'New Jersey': '34',
    'New Mexico': '35',
    'New York': '36',
    'North Carolina': '37',
    'North Dakota': '38',
    'Ohio': '39',
    'Oklahoma': '40',
    'Oregon': '41',
    'Pennsylvania': '42',
    'Rhode Island': '44',
    'South Carolina': '45',
    'South Dakota': '46',
    'Tennessee': '47',
    'Texas': '48',
    'Utah': '49',
    'Vermont': '50',
    'Virginia': '51',
    'Washington': '53',
    'West Virginia': '54',
    'Wisconsin': '55',
    'Wyoming': '56',
}


def _ensure_year(df: pd.DataFrame, date_col: str = 'Date Local') -> pd.Series:
    if date_col not in df.columns:
        msg = (
            "Missing date column '"
            + str(date_col)
            + "' to derive year for population join"
        )
        raise KeyError(msg)
    return pd.to_datetime(df[date_col]).dt.year


def enrich_with_centroids(
    df: pd.DataFrame,
    *,
    centroids_path: Path | str = Path('data/processed/city_centroids.json'),
    state_col: str = 'State',
    county_col: str = 'County',
    city_col: str = 'City',
    lat_col: str = 'lat_city',
    lon_col: str = 'lon_city',
    source_col: str = 'coord_source_city',
) -> pd.DataFrame:
    p = Path(centroids_path)
    if not p.exists():
        return df
    centroids = load_centroids_json(p)
    return apply_city_centroids(
        df,
        centroids,
        state_col=state_col,
        county_col=county_col,
        city_col=city_col,
        lat_col=lat_col,
        lon_col=lon_col,
        source_col=source_col,
    )


def enrich_with_state_population(
    df: pd.DataFrame,
    *,
    pop_path: Path | str = Path(
        'data/processed/pop_state_year_2000_2016_partial.csv'
    ),
    state_col: str = 'State',
    date_col: str = 'Date Local',
    out_col: str = 'population_state',
) -> pd.DataFrame:
    p = Path(pop_path)
    if not p.exists():
        return df
    year = _ensure_year(df, date_col)
    dfx = df.copy()
    dfx['__year'] = year
    dfx['__state_fips'] = dfx[state_col].map(STATE_NAME_TO_FIPS)

    pop = pd.read_csv(p, dtype={'state_fips': str})
    # expected columns: state_fips, year, population, name
    pop = pop.rename(columns={'population': out_col})
    dfx = dfx.merge(
        pop[['state_fips', 'year', out_col]],
        how='left',
        left_on=['__state_fips', '__year'],
        right_on=['state_fips', 'year'],
    )
    # Drop only columns that exist to avoid KeyError
    drop_cols = [c for c in ['state_fips', 'year', '__state_fips', '__year'] if c in dfx.columns]
    if drop_cols:
        dfx = dfx.drop(columns=drop_cols)
    return dfx


def _normalize_place_name(name: str) -> str:
    s = str(name).split(',')[0].strip()
    # Remove common suffixes like city, town, village, borough, CDP
    import re
    s = re.sub(
        r"\s+(city|town|village|borough|municipality|CDP|cdp)$",
        "",
        s,
        flags=re.IGNORECASE,
    )
    return normalize_city(s)


def enrich_with_city_population(
    df: pd.DataFrame,
    *,
    pop_path: Path | str = Path(
        'data/processed/pop_city_year_2000_2016_partial.csv'
    ),
    state_col: str = 'State',
    city_col: str = 'City',
    date_col: str = 'Date Local',
    out_col: str = 'population_city',
) -> pd.DataFrame:
    p = Path(pop_path)
    if not p.exists():
        return df
    year = _ensure_year(df, date_col)
    dfx = df.copy()
    dfx['__year'] = year
    if state_col == 'State':
        dfx['__state_fips'] = dfx[state_col].map(STATE_NAME_TO_FIPS).astype(str).str.zfill(2)
    else:
        dfx['__state_fips'] = dfx[state_col].astype(str).str.zfill(2)
    dfx['__year'] = dfx['__year'].astype(str)
    dfx['__city_norm'] = dfx[city_col].map(normalize_city)

    pop = pd.read_csv(p, dtype={'state_fips': str})
    # expected columns: state_fips, place_fips, year, population, name
    pop['state_fips'] = pop['state_fips'].astype(str).str.zfill(2)
    pop['year'] = pop['year'].astype(str)
    pop['__city_norm'] = pop['name'].map(_normalize_place_name)

    # Deduplicate per (state_fips, __city_norm, year); keep largest
    pop_keys = (
        pop[['state_fips', 'year', '__city_norm', 'population']]
        .sort_values(
            ['state_fips', 'year', '__city_norm', 'population'],
            ascending=[True, True, True, False],
        )
        .drop_duplicates(['state_fips', 'year', '__city_norm'], keep='first')
        .rename(columns={'population': out_col})
    )

    dfx = dfx.merge(
        pop_keys,
        how='left',
        left_on=['__state_fips', '__year', '__city_norm'],
        right_on=['state_fips', 'year', '__city_norm'],
    )
    dfx = dfx.drop(
        columns=['state_fips', 'year', '__state_fips', '__year', '__city_norm']
    )
    return dfx
