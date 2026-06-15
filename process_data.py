import marimo

__generated_with = "0.23.9"
app = marimo.App(width="wide")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # World Cider Map — Data Pipeline

    Transforms the raw **World Cider Map** spreadsheet into a clean GeoJSON
    for the Leaflet web map hosted on GitHub Pages.

    - Filters to **Active** producers only
    - Prefers Google Places-verified coordinates over manually entered values
    - Strips search-fallback URLs, keeping only verified links
    - Exports to `data/producers.geojson`
    """)
    return


@app.cell
def _(mo):
    source_path = mo.ui.text(
        value="C:/Users/Eric/Downloads/World Cider Map.xlsx",
        label="Source Excel path",
        full_width=True,
    )
    source_path
    return (source_path,)


@app.cell
def _(source_path):
    import pandas as pd
    staging = pd.read_excel(source_path.value, sheet_name="Staging")
    return (pd, staging)


@app.cell
def _(mo, staging):
    mo.hstack(
        [
            mo.stat(label="Total Records", value=f"{len(staging):,}"),
            mo.stat(label="Active", value=f"{(staging['Status'] == 'Active').sum():,}"),
            mo.stat(label="Countries", value=str(staging["Country"].nunique())),
            mo.stat(label="Producer Types", value=str(staging["Type"].nunique())),
        ],
        justify="start",
        gap=1,
    )


@app.cell
def _(mo):
    mo.md("""
    ## Coordinate Resolution

    Active records may have two sets of coordinates: manually entered (`Latitude`,
    `Longitude`) and Google Places-verified (`Places_Lat`, `Places_Long`). We
    prefer the Places values and fall back to manual when Places data is absent.
    """)
    return


@app.cell
def _(pd, staging):
    active = staging[staging["Status"] == "Active"].copy()

    active["_lat"] = pd.to_numeric(active["Places_Lat"], errors="coerce").fillna(
        pd.to_numeric(active["Latitude"], errors="coerce")
    )
    active["_lon"] = pd.to_numeric(active["Places_Long"], errors="coerce").fillna(
        pd.to_numeric(active["Longitude"], errors="coerce")
    )

    missing_coords = int(active["_lat"].isna().sum())
    active = active[active["_lat"].notna() & active["_lon"].notna()].copy()
    return (active, missing_coords)


@app.cell
def _(active, missing_coords, mo):
    mo.callout(
        mo.md(
            f"Dropped **{missing_coords}** active record(s) with no resolvable coordinates. "
            f"**{len(active):,}** producers ready to map."
        ),
        kind="warn" if missing_coords > 0 else "success",
    )


@app.cell
def _(mo):
    mo.md("""
    ## URL Cleaning

    Several link columns contain fallback Google search URLs
    (`google.com/search?q=...`) for entries where a real link hasn't been
    confirmed yet. We strip these to ensure the public GeoJSON contains only
    verified links. Platform links are also validated against their expected
    domains.
    """)
    return


@app.cell
def _(active, pd):
    def _clean_str(val):
        s = str(val).strip() if str(val) != "nan" else ""
        return s or None

    def _clean_url(val, domain=None):
        u = str(val).strip() if str(val) != "nan" else ""
        if not u or "google.com/search" in u:
            return None
        if domain and domain not in u:
            return None
        return u

    LINK_FIELDS = [
        ("website", "Website", None),
        ("google", "Google", "maps.google.com"),
        ("facebook", "Facebook", "facebook.com"),
        ("instagram", "Instagram", "instagram.com"),
        ("untappd", "Untappd", "untappd.com"),
        ("yelp", "Yelp", "yelp.com"),
        ("tripadvisor", "TripAdvisor", "tripadvisor"),
        ("glintcap", "GLINTCAP", "ciderguide.com"),
    ]

    link_quality = pd.DataFrame(
        [
            {
                "Platform": key,
                "All Links": int(active[field].notna().sum()),
                "Verified Links": int(
                    active[field].apply(lambda v: _clean_url(v, domain) is not None).sum()
                ),
            }
            for key, field, domain in LINK_FIELDS
        ]
    )
    link_quality["Fallbacks Removed"] = link_quality["All Links"] - link_quality["Verified Links"]
    return (LINK_FIELDS, _clean_str, _clean_url, link_quality)


@app.cell
def _(link_quality, mo):
    mo.ui.table(link_quality, selection=None)


@app.cell
def _(LINK_FIELDS, _clean_str, _clean_url, active, pd):
    rows = []
    for _, row in active.iterrows():
        entry = {
            "name": _clean_str(row["Name"]),
            "type": _clean_str(row["Type"]),
            "town_city": _clean_str(row["Town_City"]),
            "region": _clean_str(row["Region"]),
            "country": _clean_str(row["Country"]),
            "address": _clean_str(row["Places_Address"]),
            "alternate_name": _clean_str(row["Alternate_Name"]),
            "lat": round(float(row["_lat"]), 6),
            "lon": round(float(row["_lon"]), 6),
        }
        if pd.notna(row["ID"]):
            entry["id"] = int(row["ID"])
        for key, field, domain in LINK_FIELDS:
            v = _clean_url(row[field], domain)
            if v:
                entry[key] = v
        rows.append(entry)

    cleaned = pd.DataFrame(rows)
    return (cleaned, rows)


@app.cell
def _(mo):
    mo.md("## Explore — click a bar to filter the table")
    return


@app.cell
def _(cleaned, mo):
    import altair as alt

    type_counts = (
        cleaned.groupby("type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    chart = (
        alt.Chart(type_counts)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            x=alt.X("count:Q", title="Producers"),
            y=alt.Y("type:N", sort="-x", title=None),
            color=alt.value("#e17b2c"),
            tooltip=[
                alt.Tooltip("type:N", title="Type"),
                alt.Tooltip("count:Q", title="Count"),
            ],
        )
        .properties(height=220, width=500)
    )

    type_chart = mo.ui.altair_chart(chart)
    type_chart
    return (alt, type_chart, type_counts)


@app.cell
def _(cleaned, mo, type_chart):
    selected = type_chart.value
    if len(selected) > 0:
        preview_df = cleaned[cleaned["type"].isin(selected["type"].tolist())]
        subtitle = f"(filtered to: {', '.join(selected['type'].unique())})"
    else:
        preview_df = cleaned
        subtitle = "(select a bar above to filter)"

    mo.vstack([
        mo.md(f"**{len(preview_df):,} producers** {subtitle}"),
        mo.ui.table(
            preview_df[["name", "type", "town_city", "region", "country"]].reset_index(drop=True),
            selection=None,
            page_size=10,
        ),
    ])


@app.cell
def _(mo):
    export_btn = mo.ui.button(label="Export GeoJSON", kind="success")
    export_btn
    return (export_btn,)


@app.cell
def _(export_btn, mo, rows):
    mo.stop(
        not export_btn.value,
        mo.callout(
            mo.md("Click **Export GeoJSON** above to write `data/producers.geojson`."),
            kind="neutral",
        ),
    )

    import json
    from pathlib import Path

    output_path = Path(__file__).parent / "data" / "producers.geojson"
    output_path.parent.mkdir(exist_ok=True)

    features = []
    for entry in rows:
        lat, lon = entry.pop("lat"), entry.pop("lon")
        props = {k: v for k, v in entry.items() if v is not None}
        entry["lat"], entry["lon"] = lat, lon
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": props,
        })

    geojson = {"type": "FeatureCollection", "features": features}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = output_path.stat().st_size / 1024
    n_countries = len({e.get("country") for e in rows if e.get("country")})

    mo.callout(
        mo.md(
            f"**Exported successfully.**  \n"
            f"`{output_path}` &nbsp;·&nbsp; "
            f"{len(features):,} features &nbsp;·&nbsp; "
            f"{n_countries} countries &nbsp;·&nbsp; "
            f"{size_kb:.0f} KB"
        ),
        kind="success",
    )


if __name__ == "__main__":
    app.run()
