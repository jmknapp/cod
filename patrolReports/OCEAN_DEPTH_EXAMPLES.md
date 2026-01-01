## Ocean Depth Click Popup - Visual Examples

### Example 1: Shallow Reef Area (Dangerous Ground)
```
┌─────────────────────────────────────┐
│ Position                            │
│ 10°30.0'N 115°15.0'E               │
│ (10.50000, 115.25000)              │
│                                     │
│ Ocean Depth                         │
│ 🌊 10-100 m (reef area)            │
│ Shallow (hazardous for submarines)  │
└─────────────────────────────────────┘
Color: Brown (#d4a373)
```

### Example 2: Deep Basin (Central South China Sea)
```
┌─────────────────────────────────────┐
│ Position                            │
│ 14°20.0'N 115°30.0'E               │
│ (14.33333, 115.50000)              │
│                                     │
│ Ocean Depth                         │
│ 🌊 2000-4000 m (basin)             │
│ Deep basin (good operating depth)   │
└─────────────────────────────────────┘
Color: Dark Blue (#2c3e50)
```

### Example 3: Continental Shelf
```
┌─────────────────────────────────────┐
│ Position                            │
│ 21°15.0'N 117°45.0'E               │
│ (21.25000, 117.75000)              │
│                                     │
│ Ocean Depth                         │
│ 🌊 100-1500 m (shelf/slope)        │
│ Continental shelf/slope             │
└─────────────────────────────────────┘
Color: Blue (#3498db)
```

### Example 4: Very Deep Basin (Sulu Sea)
```
┌─────────────────────────────────────┐
│ Position                            │
│ 8°30.0'N 121°00.0'E                │
│ (8.50000, 121.00000)               │
│                                     │
│ Ocean Depth                         │
│ 🌊 4000-5000 m (deep basin)        │
│ Very deep basin                     │
└─────────────────────────────────────┘
Color: Very Dark Blue (#1a1a2e)
```

## Visual Color Guide

```
Depth       Color           Visual          Submarine Context
─────────────────────────────────────────────────────────────
0-200m      ███ Brown       Hazardous      Reefs, shoals, grounding risk
            #d4a373                        Cannot dive deep to evade

200-1000m   ███ Blue        Marginal       Continental shelf
            #3498db                        Limited diving depth

1000-3000m  ███ Dark Blue   Good           Deep basins
            #2c3e50                        Can dive to 300+ ft

3000m+      ███ Very Dark   Excellent      Very deep water
            #1a1a2e                        Maximum concealment
```

## Interactive Behavior

1. **Click** anywhere on ocean
2. **Popup appears** at click location
3. **Shows** coordinates + depth + context
4. **Click again** to see new location
5. **Previous popup closes** automatically

## Depth Zones Mapped

```
South China Sea Bathymetry Map (Simplified)

                 China
                   ║
    111°E      114°E      117°E      120°E
     │          │          │          │
20°N ┼──────────┼──────────┼──────────┼─── 20°N
     │  [200m]  │          │          │
     │  Shelf   │ Paracel  │          │
17°N ┼──────────┤ Islands  │          │─── 17°N
     │          │ [50-200m]│          │
     │          │Macclesfield         │
15°N ┼──────────┤  Bank    │  [2000m] │─── 15°N
     │          │[10-100m] │  Basin   │
     │          │          │          │Philippines
12°N ┼──────────┼──────────┤          │─── 12°N
     │          │Dangerous │          │
     │          │ Ground   │          │
10°N ┼──────────┤[10-100m] │          │─── 10°N
     │ [1000m]  │          │          │
     │  Basin   │          │  [4000m] │
 7°N ┼──────────┼──────────┼──────────┼───  7°N
     │          │          │  Sulu Sea│
     └──────────┴──────────┴──────────┘
   Vietnam    Borneo      Palawan

Legend:
[Depth] = Approximate depth range
═══ = Very deep (>3000m)
─── = Deep (1000-3000m)
··· = Shelf (200-1000m)
xxx = Shallow (<200m)
```

## Testing Locations

Try clicking these coordinates to see different depths:

| Location | Lat/Lon | Expected Depth | Color |
|----------|---------|----------------|-------|
| Dangerous Ground | 10°N, 115°E | 10-100 m | Brown |
| Macclesfield Bank | 16°N, 115°E | 10-100 m | Brown |
| Central Basin | 14°N, 115°E | 2000-4000 m | Dark Blue |
| Sulu Sea | 8°N, 121°E | 4000-5000 m | Very Dark |
| Philippine Shelf | 14°N, 120°E | 100-1000 m | Blue |
| Northern Shelf | 21°N, 117°E | 100-1500 m | Blue |
| Vietnam Coast | 12°N, 110°E | 50-500 m | Blue |

## USS Cod Context

USS Cod (SS-224) specifications:
- **Test Depth**: 300 feet (~90 meters)
- **Crush Depth**: ~400 feet (~120 meters)
- **Typical Operating Depth**: 150-250 feet (45-75 meters)

The depth display helps visualize:
- ✅ Where Cod could safely dive deep (>200m water depth)
- ⚠️ Where diving was dangerous (shallow areas)
- ❌ Where grounding risk existed (<100m areas)


