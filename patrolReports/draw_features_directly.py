#!/usr/bin/env python3
"""
Example: Drawing nautical features directly as Folium polygons
without using GeoJSON overlay layers.
"""

import folium
import json

# Option 1: Extract from existing GeoJSON file
def extract_polygons_from_geojson(geojson_file):
    """Extract polygon coordinates from GeoJSON file"""
    with open(geojson_file, 'r') as f:
        data = json.load(f)
    
    features = []
    for feature in data['features']:
        geom_type = feature['geometry']['type']
        
        if geom_type == 'Polygon':
            # Polygon: coordinates[0] is the outer ring
            coords = feature['geometry']['coordinates'][0]
            # Convert from [lon, lat] (GeoJSON) to [lat, lon] (Folium)
            folium_coords = [(lat, lon) for lon, lat in coords]
            
            features.append({
                'name': feature['properties']['name'],
                'description': feature['properties'].get('description', ''),
                'hazard': feature['properties'].get('hazard', 'Unknown'),
                'coords': folium_coords,
                'type': 'polygon'
            })
        elif geom_type == 'Point':
            # Skip points for polygon drawing
            continue
        elif geom_type == 'LineString':
            # Skip lines for polygon drawing
            continue
    
    return features

# Option 2: Manually defined polygons (if you don't have GeoJSON)
MANUAL_FEATURES = {
    'Macclesfield Bank': {
        'coords': [
            (16.5, 114.0),
            (16.5, 115.5),
            (15.5, 115.8),
            (15.0, 114.3),
            (16.5, 114.0)  # Close polygon
        ],
        'description': 'Submerged atoll, 130km x 70km, depths 11.6-100m',
        'hazard': 'High',
        'depth_range': '10-100m'
    },
    'Dangerous Ground': {
        'coords': [
            (12.0, 113.0),
            (12.0, 117.0),
            (7.5, 117.0),
            (7.5, 113.0),
            (12.0, 113.0)
        ],
        'description': 'Numerous reefs, atolls, and low islands',
        'hazard': 'Extreme',
        'depth_range': '5-200m'
    },
    'Paracel Islands': {
        'coords': [
            (17.5, 111.0),
            (17.5, 113.0),
            (15.5, 113.0),
            (15.5, 111.0),
            (17.5, 111.0)
        ],
        'description': 'Group of islands and reefs',
        'hazard': 'High',
        'depth_range': '20-150m'
    }
}

# Create map
m = folium.Map(
    location=[12.0, 115.0],  # Center on South China Sea
    zoom_start=6,
    tiles='OpenStreetMap'
)

# Option A: Draw from extracted GeoJSON data
try:
    features = extract_polygons_from_geojson('static/geojson/south_china_sea_features.json')
    
    for feature in features:
        # Set color based on hazard level
        hazard = feature['hazard'].lower()
        if hazard == 'extreme':
            color = '#8B0000'  # Dark red
            fill_opacity = 0.4
        elif hazard == 'high':
            color = '#d4a373'  # Orange/tan
            fill_opacity = 0.3
        else:
            color = '#FFD700'  # Gold
            fill_opacity = 0.2
        
        # Draw the polygon
        folium.Polygon(
            locations=feature['coords'],
            color=color,
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=fill_opacity,
            popup=folium.Popup(
                f"<b>{feature['name']}</b><br>"
                f"{feature['description']}<br>"
                f"<span style='color:{color};'>⚠ Hazard: {feature['hazard']}</span>",
                max_width=250
            ),
            tooltip=f"{feature['name']} ({feature['hazard']} hazard)"
        ).add_to(m)
    
    print(f"✅ Drew {len(features)} features from GeoJSON")
    
except FileNotFoundError:
    print("⚠ GeoJSON file not found, using manual coordinates...")
    
    # Option B: Draw from manual coordinates
    for name, data in MANUAL_FEATURES.items():
        # Set color based on hazard level
        hazard = data['hazard'].lower()
        if hazard == 'extreme':
            color = '#8B0000'
            fill_opacity = 0.4
        elif hazard == 'high':
            color = '#d4a373'
            fill_opacity = 0.3
        else:
            color = '#FFD700'
            fill_opacity = 0.2
        
        folium.Polygon(
            locations=data['coords'],
            color=color,
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=fill_opacity,
            popup=folium.Popup(
                f"<b>{name}</b><br>"
                f"{data['description']}<br>"
                f"Depth: {data['depth_range']}<br>"
                f"<span style='color:{color};'>⚠ Hazard: {data['hazard']}</span>",
                max_width=250
            ),
            tooltip=f"{name} ({data['hazard']} hazard)"
        ).add_to(m)
    
    print(f"✅ Drew {len(MANUAL_FEATURES)} features from manual coordinates")

# Save map
output_file = 'static/features_as_polygons.html'
m.save(output_file)
print(f"\n✅ Map saved to: {output_file}")
print("\nFeatures are drawn as direct Folium polygons (not GeoJSON overlay)")

