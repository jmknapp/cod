# 📍 Getting Polygon Data for Nautical Features

## Quick Answer

**You already have it!** The GeoJSON files I created contain polygon coordinates. Just extract them:

```python
import json

with open('static/geojson/south_china_sea_features.json', 'r') as f:
    data = json.load(f)

for feature in data['features']:
    coords = feature['geometry']['coordinates'][0]
    # Convert from [lon, lat] to [lat, lon] for Folium
    folium_coords = [(lat, lon) for lon, lat in coords]
    print(f"{feature['properties']['name']}: {folium_coords}")
```

---

## Data Sources for Custom Polygons

### 1. OpenStreetMap (Best for Islands/Named Features)

**Overpass Turbo**: https://overpass-turbo.eu/

Example query for Macclesfield Bank:
```
[out:json];
(
  node["name"="Macclesfield Bank"];
  way["name"="Macclesfield Bank"];
  relation["name"="Macclesfield Bank"];
);
out geom;
```

**Python API**:
```python
import requests

def get_osm_feature(name):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      way["name"="{name}"];
      relation["name"="{name}"];
    );
    out geom;
    """
    response = requests.post(overpass_url, data={'data': query})
    return response.json()
```

### 2. GEBCO Bathymetry (Best for Underwater Features)

**GEBCO Grid**: https://www.gebco.net/data_and_products/gridded_bathymetry_data/

Download the grid and trace depth contours:
```python
from netCDF4 import Dataset
import numpy as np
from skimage import measure

# Load GEBCO data
nc = Dataset('GEBCO_2023.nc')
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:]
elevation = nc.variables['elevation'][:]

# Find 100m depth contour (for shallow banks)
contours = measure.find_contours(elevation, -100)

# Convert to coordinates
for contour in contours:
    coords = [(lats[int(y)], lons[int(x)]) for y, x in contour]
```

### 3. NOAA Nautical Charts (Best for Historical Accuracy)

**NOAA ENC**: https://charts.noaa.gov/

Download Electronic Navigational Charts (ENC) in S-57 format, which includes polygon data for:
- Reefs
- Banks
- Shoals
- Dangerous areas

### 4. Natural Earth Data (Best for Quick Polygons)

**Download**: https://www.naturalearthdata.com/

```bash
# Download reefs and atolls
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_reefs.zip
unzip ne_10m_reefs.zip
```

Then read with `geopandas`:
```python
import geopandas as gpd

reefs = gpd.read_file('ne_10m_reefs.shp')
# Filter for South China Sea
scs_reefs = reefs.cx[110:125, 5:25]  # Bounding box
```

### 5. Google Earth/Maps (Manual Digitization)

1. Open Google Earth
2. Find Macclesfield Bank
3. Use the **Polygon tool** to trace the feature
4. Right-click → **Save Place As** → Save as KML
5. Convert KML to coordinates:

```python
from fastkml import kml

def kml_to_coords(kml_file):
    with open(kml_file, 'rb') as f:
        k = kml.KML()
        k.from_string(f.read())
        
    for feature in k.features():
        for placemark in feature.features():
            if placemark.geometry:
                coords = list(placemark.geometry.exterior.coords)
                return [(lat, lon) for lon, lat, *_ in coords]
```

### 6. Historical Charts (Most Accurate for WWII)

**USNO Historical Charts**: Contact Naval History and Heritage Command

For USS Cod's patrol area, use charts from 1944:
- H.O. 5374 - South China Sea
- H.O. 2750 - Philippine Islands
- British Admiralty Chart 2660 - Dangerous Ground

Scan and digitize using:
- **QGIS**: Open source GIS tool
- **MapAnalyst**: For georeferencing historical maps

---

## Drawing Polygons in Your Code

### Direct Integration into `generate_patrol_map.py`

Add this function to your map generation script:

```python
def add_nautical_features(m):
    """Add nautical features as direct polygons"""
    
    features = {
        'Macclesfield Bank': {
            'coords': [(16.5, 114.0), (16.5, 115.5), (15.5, 115.8), 
                      (15.0, 114.3), (16.5, 114.0)],
            'hazard': 'High',
            'depth': '10-100m'
        },
        'Dangerous Ground': {
            'coords': [(12.0, 113.0), (12.0, 117.0), (7.5, 117.0),
                      (7.5, 113.0), (12.0, 113.0)],
            'hazard': 'Extreme',
            'depth': '5-200m'
        }
    }
    
    for name, data in features.items():
        hazard_colors = {
            'Extreme': '#8B0000',
            'High': '#d4a373',
            'Moderate': '#FFD700'
        }
        
        color = hazard_colors.get(data['hazard'], '#999')
        
        folium.Polygon(
            locations=data['coords'],
            color=color,
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.3,
            popup=f"<b>{name}</b><br>Depth: {data['depth']}<br>Hazard: {data['hazard']}",
            tooltip=name
        ).add_to(m)
```

Then call it after creating the map:
```python
m = folium.Map(...)
add_nautical_features(m)
```

---

## Comparison: GeoJSON Overlay vs Direct Polygons

### GeoJSON Overlay
- ✅ Cleaner code
- ✅ Easier to update data
- ✅ Can toggle on/off
- ✅ Standard format

### Direct Polygons
- ✅ More control over styling
- ✅ No separate file needed
- ✅ Easier to customize per-polygon
- ✅ Simpler debugging

**Recommendation**: Use **direct polygons** if:
- You have < 20 features
- You want custom styling per feature
- You want everything in one script

Use **GeoJSON overlay** if:
- You have many features (50+)
- You want to reuse data elsewhere
- You need layer controls

---

## Example Script

I've created `draw_features_directly.py` which shows both methods:
1. Extracting coordinates from your existing GeoJSON file
2. Using manually-defined coordinate arrays

Run it:
```bash
python3 draw_features_directly.py
```

This will generate `static/features_as_polygons.html` showing all features drawn as direct Folium polygons.

---

## Quick Start

**Option 1: Use existing GeoJSON data**
```python
# Already have coordinates in:
# static/geojson/south_china_sea_features.json
```

**Option 2: Get from OpenStreetMap**
```bash
# Visit: https://overpass-turbo.eu/
# Search for feature name
# Export as GeoJSON
```

**Option 3: Digitize manually**
```
# Use Google Earth Pro
# Trace polygon
# Export as KML
# Convert to coordinates
```

The easiest is **Option 1** - you already have accurate coordinates!


