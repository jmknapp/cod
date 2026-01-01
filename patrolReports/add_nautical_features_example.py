"""
Example code to add to generate_patrol_map.py to overlay nautical features.

Add this after creating the base map but before adding patrol tracks.
"""

import os
import json

def add_nautical_features(m):
    """Add GeoJSON overlays for South China Sea features."""
    
    # Define the path to GeoJSON files
    geojson_dir = os.path.join(os.path.dirname(__file__), 'static', 'geojson')
    
    # 1. OCEAN BOTTOM FEATURES (reefs, banks, shoals)
    features_file = os.path.join(geojson_dir, 'south_china_sea_features.json')
    if os.path.exists(features_file):
        with open(features_file, 'r') as f:
            features_data = json.load(f)
        
        # Create feature group (can be toggled on/off)
        ocean_features = folium.FeatureGroup(
            name='Ocean Features (Reefs, Banks, Shoals)',
            show=True  # Show by default
        )
        
        # Style function for different feature types
        def feature_style(feature):
            hazard = feature['properties'].get('hazard_level', 'medium')
            colors = {
                'extreme': {'fill': '#e74c3c', 'line': '#c0392b'},
                'high': {'fill': '#d4a373', 'line': '#8b6f47'},
                'medium': {'fill': '#f39c12', 'line': '#d68910'}
            }
            color_scheme = colors.get(hazard, colors['medium'])
            
            return {
                'fillColor': color_scheme['fill'],
                'color': color_scheme['line'],
                'weight': 2,
                'fillOpacity': 0.25,
                'dashArray': '5, 5' if hazard == 'extreme' else None
            }
        
        # Add GeoJSON with custom popups
        folium.GeoJson(
            features_data,
            name='Ocean Features',
            style_function=feature_style,
            tooltip=folium.GeoJsonTooltip(
                fields=['name', 'type', 'hazard_level'],
                aliases=['Name:', 'Type:', 'Hazard:'],
                sticky=False
            ),
            popup=folium.GeoJsonPopup(
                fields=['name', 'description', 'historical_note'],
                aliases=['<b>Name</b>:', '<b>Description</b>:', '<b>WWII Note</b>:'],
                max_width=300
            )
        ).add_to(ocean_features)
        
        ocean_features.add_to(m)
    
    # 2. SHIPPING LANES
    lanes_file = os.path.join(geojson_dir, 'shipping_lanes.json')
    if os.path.exists(lanes_file):
        with open(lanes_file, 'r') as f:
            lanes_data = json.load(f)
        
        shipping_lanes = folium.FeatureGroup(
            name='WWII Shipping Lanes',
            show=False  # Hidden by default (can clutter map)
        )
        
        def lane_style(feature):
            traffic = feature['properties'].get('traffic', 'medium')
            widths = {
                'very_high': 3,
                'high': 2.5,
                'medium': 2
            }
            return {
                'color': '#9b59b6',  # Purple
                'weight': widths.get(traffic, 2),
                'opacity': 0.6,
                'dashArray': '10, 10'
            }
        
        folium.GeoJson(
            lanes_data,
            name='Shipping Lanes',
            style_function=lane_style,
            tooltip=folium.GeoJsonTooltip(
                fields=['name', 'traffic'],
                aliases=['Route:', 'Traffic:'],
                sticky=False
            ),
            popup=folium.GeoJsonPopup(
                fields=['name', 'description', 'historical_note'],
                aliases=['<b>Route</b>:', '<b>Description</b>:', '<b>WWII Note</b>:'],
                max_width=300
            )
        ).add_to(shipping_lanes)
        
        shipping_lanes.add_to(m)
    
    # 3. STRATEGIC AREAS (naval bases, chokepoints)
    strategic_file = os.path.join(geojson_dir, 'strategic_areas.json')
    if os.path.exists(strategic_file):
        with open(strategic_file, 'r') as f:
            strategic_data = json.load(f)
        
        strategic_areas = folium.FeatureGroup(
            name='Strategic Areas (Bases, Chokepoints)',
            show=True
        )
        
        def strategic_style(feature):
            feat_type = feature['properties'].get('type', 'other')
            if feat_type == 'naval_base':
                return {
                    'radius': 8,
                    'fillColor': '#e74c3c',
                    'color': '#c0392b',
                    'weight': 2,
                    'fillOpacity': 0.6
                }
            else:  # strategic_waterway
                return {
                    'fillColor': '#3498db',
                    'color': '#2980b9',
                    'weight': 2,
                    'fillOpacity': 0.2,
                    'dashArray': '3, 6'
                }
        
        folium.GeoJson(
            strategic_data,
            name='Strategic Areas',
            style_function=strategic_style,
            marker=folium.CircleMarker(radius=8),  # For point features
            tooltip=folium.GeoJsonTooltip(
                fields=['name', 'type'],
                aliases=['Name:', 'Type:'],
                sticky=False
            ),
            popup=folium.GeoJsonPopup(
                fields=['name', 'description', 'strategic_value', 'historical_note'],
                aliases=['<b>Name</b>:', '<b>Description</b>:', '<b>Strategic Value</b>:', '<b>WWII Note</b>:'],
                max_width=320
            )
        ).add_to(strategic_areas)
        
        strategic_areas.add_to(m)
    
    return m


# ===== INTEGRATION EXAMPLE =====
# In your generate_patrol_map.py main function, add after creating the map:

def create_map(positions):
    """Create a Folium map with patrol tracks."""
    
    # Create base map (your existing code)
    m = folium.Map(
        location=[12.0, 118.0],
        zoom_start=5,
        tiles='OpenStreetMap',
        # ... your existing map settings ...
    )
    
    # ADD THIS: Overlay nautical features
    m = add_nautical_features(m)
    
    # Then continue with your existing code to add patrol tracks, markers, etc.
    # ...
    
    # At the end, add LayerControl to toggle layers
    folium.LayerControl(
        collapsed=False,
        position='topright'
    ).add_to(m)
    
    return m


