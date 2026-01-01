#!/usr/bin/env python3
"""
Quick preview script to visualize the GeoJSON nautical features.
Run this to generate a standalone preview map.
"""

import folium
import json
import os

def create_preview_map():
    """Create a preview map with all nautical features."""
    
    # Create base map centered on South China Sea
    m = folium.Map(
        location=[12.0, 116.0],  # Center of South China Sea
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    geojson_dir = os.path.join(os.path.dirname(__file__), 'static', 'geojson')
    
    # 1. Ocean Features
    print("Loading ocean features...")
    with open(os.path.join(geojson_dir, 'south_china_sea_features.json'), 'r') as f:
        features_data = json.load(f)
    
    ocean_features = folium.FeatureGroup(name='🌊 Ocean Features', show=True)
    
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
    
    folium.GeoJson(
        features_data,
        style_function=feature_style,
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'type', 'hazard_level'],
            aliases=['Name:', 'Type:', 'Hazard:']
        ),
        popup=folium.GeoJsonPopup(
            fields=['name', 'description', 'historical_note'],
            aliases=['<b>Feature</b>:', '<b>Description</b>:', '<b>WWII Context</b>:'],
            max_width=350
        )
    ).add_to(ocean_features)
    ocean_features.add_to(m)
    
    # 2. Shipping Lanes
    print("Loading shipping lanes...")
    with open(os.path.join(geojson_dir, 'shipping_lanes.json'), 'r') as f:
        lanes_data = json.load(f)
    
    shipping_lanes = folium.FeatureGroup(name='🚢 Shipping Lanes (WWII)', show=True)
    
    def lane_style(feature):
        traffic = feature['properties'].get('traffic', 'medium')
        widths = {'very_high': 3, 'high': 2.5, 'medium': 2}
        return {
            'color': '#9b59b6',
            'weight': widths.get(traffic, 2),
            'opacity': 0.6,
            'dashArray': '10, 10'
        }
    
    folium.GeoJson(
        lanes_data,
        style_function=lane_style,
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'traffic'],
            aliases=['Route:', 'Traffic Level:']
        ),
        popup=folium.GeoJsonPopup(
            fields=['name', 'description', 'historical_note'],
            aliases=['<b>Route</b>:', '<b>Description</b>:', '<b>WWII Context</b>:'],
            max_width=350
        )
    ).add_to(shipping_lanes)
    shipping_lanes.add_to(m)
    
    # 3. Strategic Areas
    print("Loading strategic areas...")
    with open(os.path.join(geojson_dir, 'strategic_areas.json'), 'r') as f:
        strategic_data = json.load(f)
    
    strategic_areas = folium.FeatureGroup(name='⚓ Strategic Areas', show=True)
    
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
        else:
            return {
                'fillColor': '#3498db',
                'color': '#2980b9',
                'weight': 2,
                'fillOpacity': 0.2,
                'dashArray': '3, 6'
            }
    
    folium.GeoJson(
        strategic_data,
        style_function=strategic_style,
        marker=folium.CircleMarker(radius=8),
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'type', 'strategic_value'],
            aliases=['Name:', 'Type:', 'Strategic Value:']
        ),
        popup=folium.GeoJsonPopup(
            fields=['name', 'description', 'historical_note'],
            aliases=['<b>Location</b>:', '<b>Description</b>:', '<b>WWII Context</b>:'],
            max_width=350
        )
    ).add_to(strategic_areas)
    strategic_areas.add_to(m)
    
    # Add layer control
    folium.LayerControl(collapsed=False, position='topright').add_to(m)
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 400px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <h4 style="margin:0">South China Sea Nautical Features</h4>
    <p style="margin:5px 0">Preview of GeoJSON overlays for USS Cod patrol map</p>
    <p style="margin:5px 0; font-size:11px; color:#666">
    Click features for details. Use layer control (top right) to toggle layers.
    </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save
    output_file = os.path.join(os.path.dirname(__file__), 'static', 'nautical_features_preview.html')
    m.save(output_file)
    print(f"\n✅ Preview map saved to: {output_file}")
    print("Open this file in a web browser to view the features.")
    
    return m

if __name__ == '__main__':
    create_preview_map()


