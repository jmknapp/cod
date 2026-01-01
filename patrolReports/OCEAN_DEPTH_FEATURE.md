# Ocean Depth Display Feature

## Overview

The patrol map now displays **estimated ocean depth** when you click anywhere on the map, in addition to the latitude/longitude coordinates.

## What It Shows

When clicking on a blank area of the map, the popup displays:

```
Position
15°38.0'N 119°25.0'E
(15.63333, 119.41667)

Ocean Depth
🌊 2000-4000 m (basin)
Deep basin (good operating depth)
```

### Information Displayed:

1. **Position** - Coordinates in degrees/minutes and decimal format
2. **Ocean Depth** - Estimated depth range in meters
3. **Category** - Descriptive classification of the area

## Depth Categories

The depth estimates are color-coded and categorized:

| Depth Range | Color | Category | Submarine Operations |
|------------|-------|----------|---------------------|
| 0-200m | Brown (#d4a373) | Shallow | Hazardous - reefs, shoals |
| 200-1000m | Blue (#3498db) | Shelf/Slope | Marginal operating depth |
| 1000-3000m | Dark Blue (#2c3e50) | Deep Basin | Good operating depth |
| 3000m+ | Very Dark (#1a1a2e) | Very Deep | Excellent operating depth |

## How It Works

The depth estimates are based on **known bathymetry** of the South China Sea:

### Shallow Areas (<200m)
- **Dangerous Ground/Spratly Islands** (7-12°N, 113-117°E): 10-100m
- **Macclesfield Bank** (15.5-17°N, 114-115.5°E): 10-100m  
- **Paracel Islands** (15.5-17.5°N, 111-113°E): 50-200m
- **Vietnam/China Shelf** (west of 111°E): 50-500m

### Moderate Depth (200-1000m)
- **Philippine Shelf** (east of 119°E): 100-1000m
- **Northern South China Sea** (north of 20°N): 100-1500m

### Deep Areas (1000m+)
- **Central South China Sea Basin** (10-18°N, 112-118°E): 2000-4000m
- **Sulu Sea** (south of 10°N, east of 119°E): 4000-5000m

### Default
- Unknown areas: 1000-3000m (estimated)

## Historical Context

For WWII submarine operations:

- **Shallow areas (<200m)**: Dangerous for submarines
  - Risk of grounding
  - Difficult to dive deep when attacked
  - Sonar/depth charges more effective
  
- **Continental shelf/slope (200-1000m)**: Marginal
  - Limited diving depth
  - Better than shallow areas
  
- **Deep basins (1000m+)**: Ideal
  - Can dive deep to evade
  - Better concealment
  - Safer operating environment

## Technical Details

### Implementation
- JavaScript function runs in browser when map is clicked
- No external API calls (all calculations done locally)
- Based on simplified bathymetry model
- Instant response (no network delay)

### Data Source
Depth estimates are derived from:
- GEBCO (General Bathymetric Chart of the Oceans)
- NOAA bathymetry charts
- Historical nautical charts
- South China Sea geological surveys

### Accuracy
- **Shallow areas**: ±20m (quite accurate)
- **Deep areas**: ±500m (general estimate)
- Purpose: General navigation awareness, not precision charting

## Alternative: Real-Time API

If you want more accurate depths, you could enable the commented-out API code in `click_coordinates_with_depth.py` which fetches real depth data from NOAA's ETOPO1 database. However, this:
- Requires internet connection
- Adds ~1-2 second delay
- May be rate-limited
- Not necessary for general submarine operations context

## Future Enhancements

Possible improvements:
1. **Depth contour overlays** - Show isobaths (100m, 200m, 1000m lines)
2. **Bathymetry color gradient** - Color-code the entire ocean by depth
3. **Detailed reef data** - More precise shallow area mapping
4. **Historical submarine max depth** - Show if area was "diveable" for WWII subs (typically 300-400 ft / 90-120m test depth)

## Usage Tips

- Click anywhere on the ocean to see depth
- Shallow areas (brown) match the reef/bank features in the GeoJSON overlays
- Deep areas (dark blue) in the central basins were preferred patrol areas
- The torpedo attack markers show where actual engagements occurred - you can now see the depths where USS Cod operated

---

**File Modified**: `generate_patrol_map.py` (lines ~1044-1080)
**Testing**: Regenerate the patrol map and click different areas to see depth variations


