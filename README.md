# World Cider Map

An interactive web map of cider producers worldwide, rebuilt as a portfolio project showcasing modern data and cartography skills.

**Live map →** [ericallanwest.github.io/ciderguide](https://ericallanwest.github.io/ciderguide)

## What's here

| File | Purpose |
|---|---|
| `index.html` | Leaflet.js web map — hand-crafted HTML/CSS/JS |
| `process_data.py` | Marimo reactive notebook — data pipeline from raw spreadsheet to GeoJSON |
| `data/producers.geojson` | Clean, open data — 3,054 producers across 62 countries |

## Data

The underlying dataset has been maintained since the early 2010s, tracking cider producers worldwide. Each record includes:

- Name, type, and location (city / region / country)
- Verified coordinates (Google Places API)
- Links to Website, Google Maps, Untappd, Instagram, Facebook, Yelp, TripAdvisor, and CiderGuide

**Producer types:** Cider · Wine · Beer · Mead · Fruit Wine · Spirits · Point of Interest

The GeoJSON is freely available for reuse under the terms of the project license.

## Running the data pipeline

The notebook reads the source Excel file and exports `data/producers.geojson`.

```bash
pip install marimo pandas openpyxl altair
marimo edit process_data.py
```

Update the **Source Excel path** field at the top of the notebook, then click **Export GeoJSON**.

## Tech stack

- **[Leaflet.js](https://leafletjs.com/)** — interactive map
- **[Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster)** — marker clustering for 3k+ points
- **[CartoDB basemaps](https://carto.com/basemaps/)** — clean cartographic base
- **[Marimo](https://marimo.io/)** — reactive Python notebook for the data pipeline
- **[Altair](https://altair-viz.github.io/)** — declarative charts in the notebook
- **GitHub Pages** — static hosting

## History

This map has lived in various homes over the years, including ArcGIS Online and Felt. This version rebuilds it as open, self-hosted, and reproducible.

---

## Prior work (ArcGIS Online & Tableau)

### ArcGIS Online
- [World Cider Map](https://arcg.is/8vnbm1)
- [Great Lakes International Cider & Perry Competition (GLINTCAP)](https://arcg.is/1S1SHq1)
- [Northwest Cider Cup](https://arcg.is/jKCTy1)
- [Cidercraft Awards](https://arcg.is/1v8SO91)
- [Good Food Awards](https://arcg.is/jHuLP0)
- [Royal Bath & West Show – British Cider Championships](https://arcg.is/ieX9r0)
- [International Cider Awards](https://arcg.is/1OSuCb2)
- [International Cider Challenge](https://arcg.is/15q9Hm1)
- [Australian Cider Awards](https://arcg.is/zTX0X)
- [CiderWorld Awards](https://arcg.is/0frD48)
- [Concours Général Agricole](https://arcg.is/1OzbjW2)
- [Concours des Cidres de Normandie](https://arcg.is/G85Ly1)
- [Concours Régional Cidricole de Bretagne](https://arcg.is/0aWnWb0)
- [Sagardo Forum International Cider Competition](https://arcg.is/1yDneX2)
- [Salón Internacional de les Sidres de Gala Awards (SISGA)](https://arcg.is/1mjH9D1)
- [Japan Cider Cup](https://arcg.is/9qKuC0)

### Tableau
- [Worldwide Cider Competitions](https://public.tableau.com/views/CiderCompetitionsDraft20240926/MedalistsMap)
- [GLINTCAP Commercial Medalists](https://public.tableau.com/views/GLINTCAPCommercialMedalists2005-2024/MedalistsMap)
- [Cidercraft Awards](https://public.tableau.com/views/CidercraftAwards/MedalistsMap)
- [The Cider Insider by Susanna Forbes](https://public.tableau.com/views/TheCiderInsider/TheCiderInsiderbySusannaForbes)
