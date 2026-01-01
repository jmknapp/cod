# South China Sea GeoJSON Features

This directory contains GeoJSON files for overlaying nautical and strategic features on the USS Cod patrol map.

## Files

### 1. `south_china_sea_features.json`
Ocean bottom features that were navigation hazards:
- **Macclesfield Bank** - Submerged atoll (130km x 70km), depths 11-100m
- **Dangerous Ground** - Large hazard zone with reefs and shoals (Spratly area)
- **Scarborough Shoal** - Reef west of Luzon
- **Paracel Islands** - Island group, Japanese-occupied WWII
- **Pratas Reef** - Atoll with Japanese seaplane base
- **Reed Bank** - Submerged atoll in Spratly area

**Display**: Show by default with semi-transparent fill
**Color scheme**: 
- Extreme hazard: Red (#e74c3c)
- High hazard: Brown/tan (#d4a373)
- Medium hazard: Orange (#f39c12)

### 2. `shipping_lanes.json`
Major WWII Japanese shipping routes:
- **Manila - Hong Kong** - Major convoy route
- **Singapore - Manila** - Critical supply line (heavily patrolled)
- **Formosa - Luzon** - Coastal route along eastern SCS
- **Indochina - Singapore** - Resource transport route
- **Cam Ranh Bay - Manila** - From major Japanese naval base

**Display**: Hidden by default (can clutter map)
**Color scheme**: Purple (#9b59b6) dashed lines
**Line width**: Varies by traffic volume (2-3 pixels)

### 3. `strategic_areas.json`
Strategic waterways and naval bases:
- **Luzon Strait** - Critical chokepoint (SCS to Pacific)
- **Balabac Strait** - Gateway to Sulu Sea
- **Mindoro Strait** - Approach to Manila Bay
- **Cam Ranh Bay** - Major Japanese fleet base
- **Manila Bay** - Major port (Japanese-occupied)
- **Subic Bay** - Former US naval base

**Display**: Show by default
**Color scheme**:
- Naval bases: Red circles (#e74c3c)
- Straits/waterways: Blue semi-transparent (#3498db)

## Usage

See `add_nautical_features_example.py` for integration code.

```python
from add_nautical_features_example import add_nautical_features

# After creating your base map:
m = add_nautical_features(m)
```

## Sources

- Wikipedia: Macclesfield Bank, Dangerous Ground, Paracel Islands
- Historical WWII submarine patrol records
- Nautical charts and navigation hazard databases
- US Department of State maritime boundaries data

## Notes

- Coordinates are approximate for historical features
- Some boundaries are simplified for display purposes
- Shipping lanes represent general routes, not exact tracks
- All features were relevant to WWII submarine operations 1942-1945

## Future Enhancements

Potential additions:
- More detailed reef outlines
- Depth contours (bathymetry)
- Historical minefield locations
- Japanese patrol areas
- Additional ports and anchorages
- Coastal defense zones


