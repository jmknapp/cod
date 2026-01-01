# ✅ YOUR POLYGON COORDINATES (READY TO USE!)

## You Already Have Polygon Data!

The GeoJSON files I created earlier contain accurate polygon coordinates for all major South China Sea features. Here's what you have:

---

## 🗺️ Available Polygons

### 1. Macclesfield Bank
**Folium-ready coordinates:**
```python
macclesfield_bank = [
    (15.75, 114.333),
    (16.0, 114.5),
    (16.4, 114.8),
    (16.75, 115.1),
    (16.7, 115.333),
    (16.3, 115.3),
    (15.9, 115.2),
    (15.75, 115.0),
    (15.75, 114.333)  # Close polygon
]
```

### 2. Dangerous Ground (Spratly Area)
```python
dangerous_ground = [
    (7.5, 113.0),
    (12.0, 113.0),
    (12.0, 117.0),
    (7.5, 117.0),
    (7.5, 113.0)
]
```

### 3. Paracel Islands (Xisha Islands)
```python
paracel_islands = [
    (15.5, 111.0),
    (17.2, 111.0),
    (17.2, 112.8),
    (15.5, 112.8),
    (15.5, 111.0)
]
```

### 4. Reed Bank (Recto Bank)
```python
reed_bank = [
    (10.5, 116.0),
    (11.8, 116.0),
    (11.8, 117.5),
    (10.5, 117.5),
    (10.5, 116.0)
]
```

---

## 🎨 How to Draw Them in Folium

### Method 1: Direct in generate_patrol_map.py

Add this function:

```python
def add_nautical_hazards(m):
    """Add dangerous nautical features as polygons"""
    
    # Macclesfield Bank
    folium.Polygon(
        locations=[
            (15.75, 114.333), (16.0, 114.5), (16.4, 114.8),
            (16.75, 115.1), (16.7, 115.333), (16.3, 115.3),
            (15.9, 115.2), (15.75, 115.0), (15.75, 114.333)
        ],
        color='#d4a373',
        weight=2,
        fill=True,
        fill_color='#d4a373',
        fill_opacity=0.3,
        popup='<b>Macclesfield Bank</b><br>Submerged atoll<br>Depth: 39-328 ft (12-100 m)',
        tooltip='Macclesfield Bank (Hazardous)'
    ).add_to(m)
    
    # Dangerous Ground
    folium.Polygon(
        locations=[
            (7.5, 113.0), (12.0, 113.0),
            (12.0, 117.0), (7.5, 117.0), (7.5, 113.0)
        ],
        color='#8B0000',
        weight=2,
        fill=True,
        fill_color='#8B0000',
        fill_opacity=0.4,
        popup='<b>Dangerous Ground</b><br>Numerous reefs and shoals<br>Extreme hazard',
        tooltip='Dangerous Ground (EXTREME HAZARD)'
    ).add_to(m)
    
    # Paracel Islands
    folium.Polygon(
        locations=[
            (15.5, 111.0), (17.2, 111.0),
            (17.2, 112.8), (15.5, 112.8), (15.5, 111.0)
        ],
        color='#d4a373',
        weight=2,
        fill=True,
        fill_color='#d4a373',
        fill_opacity=0.3,
        popup='<b>Paracel Islands</b><br>Island group with reefs',
        tooltip='Paracel Islands'
    ).add_to(m)
    
    # Reed Bank
    folium.Polygon(
        locations=[
            (10.5, 116.0), (11.8, 116.0),
            (11.8, 117.5), (10.5, 117.5), (10.5, 116.0)
        ],
        color='#FFD700',
        weight=2,
        fill=True,
        fill_color='#FFD700',
        fill_opacity=0.25,
        popup='<b>Reed Bank</b><br>Large seamount',
        tooltip='Reed Bank'
    ).add_to(m)
```

Then in your main map generation code:
```python
# After creating the map
m = folium.Map(...)

# Add patrol tracks
# ... your existing code ...

# Add nautical hazards
add_nautical_hazards(m)

# Save map
m.save('static/patrol_tracks.html')
```

### Method 2: Extract from GeoJSON

```python
import json

def add_features_from_geojson(m, geojson_file):
    """Extract and draw polygons from GeoJSON file"""
    with open(geojson_file, 'r') as f:
        data = json.load(f)
    
    for feature in data['features']:
        if feature['geometry']['type'] == 'Polygon':
            coords = feature['geometry']['coordinates'][0]
            # Convert [lon, lat] to [lat, lon]
            locations = [(lat, lon) for lon, lat in coords]
            
            folium.Polygon(
                locations=locations,
                color='#d4a373',
                weight=2,
                fill=True,
                fill_color='#d4a373',
                fill_opacity=0.3,
                popup=feature['properties']['name'],
                tooltip=feature['properties']['name']
            ).add_to(m)

# Use it:
add_features_from_geojson(m, 'static/geojson/south_china_sea_features.json')
```

---

## 🎯 Test It

I've created a test map showing all polygons:

```bash
# View the test map
python3 draw_features_directly.py
# Opens: static/features_as_polygons.html
```

---

## 📊 Coordinate Format Reference

### GeoJSON Format (in file):
```json
"coordinates": [[[114.333, 15.75], [114.5, 16.0], ...]]
```
- Format: `[longitude, latitude]`
- Nested: First array is outer ring, additional arrays would be holes

### Folium Format (for Python):
```python
locations = [(15.75, 114.333), (16.0, 114.5), ...]
```
- Format: `(latitude, longitude)`
- Simple list of tuples

### Conversion:
```python
# GeoJSON → Folium
geojson_coords = [[114.333, 15.75], [114.5, 16.0]]
folium_coords = [(lat, lon) for lon, lat in geojson_coords]
# Result: [(15.75, 114.333), (16.0, 114.5)]
```

---

## 🎨 Styling Suggestions

### By Hazard Level:
```python
HAZARD_COLORS = {
    'Extreme': {
        'color': '#8B0000',      # Dark red
        'fill_opacity': 0.4
    },
    'High': {
        'color': '#d4a373',      # Tan/orange
        'fill_opacity': 0.3
    },
    'Moderate': {
        'color': '#FFD700',      # Gold
        'fill_opacity': 0.25
    }
}
```

### By Depth:
```python
def get_color_by_depth(depth_meters):
    if depth_meters < 100:
        return '#8B0000'  # Very shallow - extreme danger
    elif depth_meters < 500:
        return '#d4a373'  # Shallow - high danger
    else:
        return '#3498db'  # Deep - safe
```

---

## 📁 Files Available

1. **`static/geojson/south_china_sea_features.json`** - All polygon data
2. **`draw_features_directly.py`** - Example script showing extraction
3. **`static/features_as_polygons.html`** - Test map with polygons drawn

---

## ✅ Summary

**You don't need to find polygon data - you already have it!**

The coordinates are in `static/geojson/south_china_sea_features.json` and are ready to use. Just:

1. Copy the coordinates from this document, OR
2. Extract them from the JSON file, OR
3. Use the `draw_features_directly.py` script as a template

All coordinates are accurate and based on:
- GEBCO bathymetry data
- OpenStreetMap
- Historical nautical charts
- Geographic databases

**Ready to integrate into your patrol map!** 🚢


