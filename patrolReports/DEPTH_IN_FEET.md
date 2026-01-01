# 📏 Depth Now Displayed in FEET

## What Changed

Ocean depths are now displayed in **feet** (historically accurate for US Navy submarines), with meters shown in parentheses.

## Examples

### Precise Depth (from API):
```
Ocean Depth
🌊 942 ft (287 m)
Continental shelf (limited diving room)
(NOAA bathymetry data)
```

### Estimated Range:
```
Ocean Depth
🌊 607-2,133 ft (185-650 m)
Continental shelf (limited diving room)
(estimated from regional bathymetry)
```

### Deep Water:
```
Ocean Depth
🌊 10,498-13,123 ft (3,200-4,000 m)
Deep basin (good operating depth)
(estimated from regional bathymetry)
```

## Historical Context

### USS Cod (SS-224) Specifications:
- **Test Depth**: 300 feet (~90 meters)
- **Crush Depth**: ~400 feet (~120 meters)
- **Safe Operating Depth**: 150-250 feet (45-75 meters)

### Depth Categories:

| Depth | Feet Range | Submarine Operations |
|-------|-----------|---------------------|
| **Shallow** | < 656 ft | **Hazardous** - Less than test depth, limited escape depth |
| **Shelf** | 656-3,281 ft | **Marginal** - Some diving room but still restricted |
| **Deep** | 3,281-9,843 ft | **Good** - Ample depth for evasion and operations |
| **Very Deep** | > 9,843 ft | **Excellent** - Maximum concealment possible |

## Why Feet?

1. **Historical Accuracy**: US Navy measured depth in feet and fathoms
2. **Submarine Context**: Test depths, crush depths all specified in feet
3. **Operational Relevance**: Crew would think in feet, not meters
4. **Period Appropriate**: Makes the data match WWII submarine operations

## Example Comparisons

| Location | Meters | Feet | USS Cod Context |
|----------|--------|------|-----------------|
| Macclesfield Bank | 12-55 m | 39-180 ft | **Dangerously shallow** - Can't dive to test depth |
| Philippine Shelf | 185-650 m | 607-2,133 ft | **Marginal** - Can dive but limited |
| Central Basin | 3,200-3,850 m | 10,499-12,631 ft | **Ideal** - Deep enough for any maneuver |
| Sulu Sea | 4,200-5,100 m | 13,780-16,732 ft | **Excellent** - Maximum depth available |

## Display Format

- **Primary**: Feet (US Navy standard)
- **Secondary**: Meters in parentheses (for reference)
- **Formatting**: Comma-separated for readability (e.g., "13,780 ft")

## Deploy to Production

The map has been regenerated. To deploy:

```bash
cd /home/jmknapp/cod/patrolReports
sudo cp static/patrol_tracks.html /var/www/html/codpatrols/static/patrol_tracks.html
```

Or use the full deployment script:

```bash
sudo ./deploy.sh
```

## Test It

1. Deploy to production (command above)
2. Open patrol map in browser
3. Hard refresh: `Ctrl+Shift+R` or `Cmd+Shift+R`
4. Click on ocean
5. See depth in feet!

### Test Locations:

| Click Here | Expected Depth |
|------------|----------------|
| 10°N, 115°E (Dangerous Ground) | ~49-262 ft (15-80 m) |
| 14°N, 115°E (Central Basin) | ~10,499-12,631 ft (3,200-3,850 m) |
| 8°N, 121°E (Sulu Sea) | ~13,780-16,732 ft (4,200-5,100 m) |

## Historical Note

During WWII, submarine crews often referred to depth in **fathoms** (1 fathom = 6 feet):
- Test depth: 50 fathoms (300 ft)
- Typical operating depth: 25-40 fathoms (150-240 ft)

The display uses feet as it's more precise and commonly understood, but you can mentally convert to fathoms by dividing by 6.

---

**Status**: ✅ Regenerated with feet display  
**Ready to deploy**: Run sudo command above  
**Historical accuracy**: ✅ Matches US Navy standards


