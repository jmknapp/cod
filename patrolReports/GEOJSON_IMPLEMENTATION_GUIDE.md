# GeoJSON Nautical Features - Implementation Guide

## What I've Created

I've created a complete set of GeoJSON files and integration code to add nautical features to your USS Cod patrol map.

### Files Created

```
patrolReports/
├── static/
│   └── geojson/                          # NEW DIRECTORY
│       ├── south_china_sea_features.json # Ocean features (reefs, banks, shoals)
│       ├── shipping_lanes.json           # WWII shipping routes
│       ├── strategic_areas.json          # Naval bases and chokepoints
│       └── README.md                     # Documentation
├── add_nautical_features_example.py      # Integration code example
└── preview_nautical_features.py          # Preview/test script
```

## Features Included

### 1. Ocean Bottom Features (`south_china_sea_features.json`)
- **Macclesfield Bank** - Submerged atoll, 130km x 70km
- **Dangerous Ground** - Large hazard zone (52,000 nm²)
- **Scarborough Shoal** - Reef west of Luzon
- **Paracel Islands** - Japanese-occupied island group
- **Pratas Reef** - Atoll with Japanese seaplane base
- **Reed Bank** - Submerged atoll

**Visual**: Brown/tan polygons with semi-transparent fill

### 2. Shipping Lanes (`shipping_lanes.json`)
- Manila - Hong Kong
- Singapore - Manila (most important)
- Formosa (Taiwan) - Luzon
- Indochina - Singapore
- Cam Ranh Bay - Manila

**Visual**: Purple dashed lines (width varies by traffic)

### 3. Strategic Areas (`strategic_areas.json`)
- **Luzon Strait** - Critical chokepoint
- **Balabac Strait** - Gateway to Sulu Sea
- **Mindoro Strait** - Approach to Manila
- **Cam Ranh Bay** - Major Japanese fleet base
- **Manila Bay** - Major port
- **Subic Bay** - Naval facility

**Visual**: 
- Naval bases: Red circles
- Straits: Blue semi-transparent polygons

## Quick Start

### Option 1: Preview the Features

Test the GeoJSON files before integrating:

```bash
cd /home/jmknapp/cod/patrolReports
python3 preview_nautical_features.py
```

This creates `static/nautical_features_preview.html` - open it in a browser.

### Option 2: Integrate into Your Patrol Map

1. **Open `generate_patrol_map.py`**

2. **Add the import** (near the top):
   ```python
   import json
   ```

3. **Copy the `add_nautical_features()` function** from `add_nautical_features_example.py` into `generate_patrol_map.py`

4. **Call it in your `create_map()` function** (after creating the base map):
   ```python
   def create_map(positions):
       # Create base map
       m = folium.Map(...)
       
       # ADD THIS LINE:
       m = add_nautical_features(m)
       
       # Continue with your existing code...
   ```

5. **Regenerate the patrol map**:
   ```bash
   python3 generate_patrol_map.py
   ```

## Customization Options

### Show/Hide by Default

In the `add_nautical_features()` function:

```python
ocean_features = folium.FeatureGroup(
    name='Ocean Features',
    show=True  # Change to False to hide by default
)
```

### Change Colors

Modify the style functions:

```python
def feature_style(feature):
    return {
        'fillColor': '#YOUR_COLOR',  # Change fill color
        'color': '#YOUR_COLOR',      # Change border color
        'fillOpacity': 0.25,         # Change transparency (0-1)
    }
```

### Add More Features

Edit the JSON files directly. Format:

```json
{
  "type": "Feature",
  "id": "unique_id",
  "geometry": {
    "type": "Polygon",  // or "LineString", "Point"
    "coordinates": [[...]]
  },
  "properties": {
    "name": "Feature Name",
    "description": "Description text",
    "hazard_level": "high"  // or "medium", "extreme"
  }
}
```

## Color Scheme Reference

| Feature Type | Color | Hex Code | Use |
|--------------|-------|----------|-----|
| Extreme Hazard | Red | `#e74c3c` | Dangerous Ground |
| High Hazard | Brown/Tan | `#d4a373` | Macclesfield Bank |
| Medium Hazard | Orange | `#f39c12` | Other reefs |
| Shipping Lanes | Purple | `#9b59b6` | All routes |
| Naval Bases | Red | `#e74c3c` | Ports, anchorages |
| Straits | Blue | `#3498db` | Chokepoints |

## Historical Context

All features are relevant to WWII submarine operations (1942-1945):

- **Dangerous Ground**: Major navigation hazard for submarines. USS Darter ran aground here in 1944.
- **Macclesfield Bank**: Submerged atoll, navigation hazard
- **Luzon Strait**: Primary patrol area for interdicting Japanese convoys
- **Singapore-Manila Lane**: Most heavily patrolled route by Allied submarines
- **Cam Ranh Bay**: Major Japanese fleet anchorage, prime hunting ground

## Next Steps

1. ✅ Run `preview_nautical_features.py` to see the features
2. ⬜ Review and adjust colors/opacity if needed
3. ⬜ Integrate into `generate_patrol_map.py`
4. ⬜ Regenerate patrol map
5. ⬜ Test in browser with layer controls

## Additional Features to Consider

Future enhancements you might want to add:

- **Depth contours** (bathymetry lines)
- **Historical minefield locations**
- **Japanese patrol areas/defensive zones**
- **More ports and anchorages**
- **Island chains in more detail**
- **Coastal defense zones**
- **Aircraft patrol ranges**

## Data Sources

- Wikipedia (Macclesfield Bank, Dangerous Ground, Paracel Islands)
- WWII submarine patrol records
- Historical nautical charts
- U.S. Department of State maritime boundaries

## Questions?

The code is well-commented and follows the same patterns as your existing `generate_patrol_map.py`. The GeoJSON files are standard format and can be edited with any text editor or GIS software.


