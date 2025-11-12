# City centroids lookup (state → county → city → lat/lon)

File: `city_centroids.json`

Purpose
- Provides administrative centroids for US cities for quick, reproducible coordinate backfills.
- Intended as a coarse fallback, not precise site/location geocoding.

Data shape
- Nested mapping: `state -> normalized county -> lowercased city -> { lat, lon }`
- Example:
  ```json
  {
    "California": {
      "los angeles": {
        "los angeles": { "lat": 34.052235, "lon": -118.243683 }
      }
    }
  }
  ```

Normalization rules
- County names are normalized by removing common suffixes (e.g. " County", " Parish", " Borough", " Census Area", " Municipality", " City and Borough").
- City keys are lowercased and trimmed.
- State keys are stored as-is (trimmed), e.g., "California", "TX", etc.

How to use (from a notebook)
```python
from utils.city_centroids import load_centroids_json, apply_city_centroids

centroids = load_centroids_json('../data/processed/city_centroids.json')

# Apply to a copy of your DataFrame; customize column names if needed
# df is your input DataFrame with columns 'State', 'County', 'City'
df_coord = apply_city_centroids(
    df.copy(),  # or your existing DataFrame
    centroids,
    state_col='State',
    county_col='County',
    city_col='City',
)

# New columns added (non-destructive): 'lat_city', 'lon_city', 'coord_source_city'
df_coord[['State','County','City','lat_city','lon_city','coord_source_city']].head()
```

Regenerating the JSON (optional)
- The notebook `jupyter_notebooks/etl_extract_cood.ipynb` contains a cell under
  "Export city centroids to JSON (optional)" that rebuilds this file from your data
  using geopy/Nominatim. Run it only when you need to refresh the lookup.

Notes and caveats
- These are centroids; they are not exact addresses. Validate before using for distance analyses.
- Keep the file as strict JSON (no comments). If you need richer documentation, use this README or a sidecar metadata file.
- If you need schema validation, consider adding a `city_centroids.schema.json` and validating in code.
