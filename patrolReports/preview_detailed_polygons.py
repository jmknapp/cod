#!/usr/bin/env python3
"""
Preview the detailed polygons we have so far.
Shows the difference between simple rectangles and detailed outlines.
"""

import folium
import json

# Create map centered on South China Sea
m = folium.Map(
    location=[12.0, 116.0],
    zoom_start=6,
    tiles='OpenStreetMap'
)

# Add satellite layer
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite',
    overlay=False,
    control=True
).add_to(m)

print("Loading detailed features...")

# Load and display detailed features
try:
    with open('static/geojson/detailed_features.json', 'r') as f:
        data = json.load(f)
    
    for feature in data['features']:
        name = feature['properties']['name']
        coords = feature['geometry']['coordinates'][0]
        locations = [(lat, lon) for lon, lat in coords]
        
        # Draw detailed polygon in green
        folium.Polygon(
            locations=locations,
            color='#00ff00',  # Bright green
            weight=2,
            fill=True,
            fill_color='#00ff00',
            fill_opacity=0.3,
            popup=f"<b>{name}</b><br>DETAILED: {len(coords)} points<br>(from OpenStreetMap)",
            tooltip=f"{name} - DETAILED ({len(coords)} points)"
        ).add_to(m)
        
        print(f"✅ {name}: {len(coords)} points (DETAILED)")

except FileNotFoundError:
    print("⚠️  No detailed features file found")

# Also show the simple versions for comparison
print("\nAdding simple rectangles for comparison...")

simple_features = {
    'Macclesfield Bank (SIMPLE)': {
        'coords': [(15.5, 114.0), (16.5, 114.0), (16.5, 115.5), (15.5, 115.5), (15.5, 114.0)],
        'points': 5
    },
    'Dangerous Ground (SIMPLE)': {
        'coords': [(7.5, 113.0), (12.0, 113.0), (12.0, 117.0), (7.5, 117.0), (7.5, 113.0)],
        'points': 5
    },
    'Paracel Islands (SIMPLE)': {
        'coords': [(15.5, 111.0), (17.5, 111.0), (17.5, 113.0), (15.5, 113.0), (15.5, 111.0)],
        'points': 5
    }
}

for name, data in simple_features.items():
    folium.Polygon(
        locations=data['coords'],
        color='#ff0000',  # Red
        weight=2,
        fill=True,
        fill_color='#ff0000',
        fill_opacity=0.15,
        popup=f"<b>{name}</b><br>SIMPLE: {data['points']} points<br>(rectangle approximation)",
        tooltip=f"{name} ({data['points']} points)",
        dashArray='5, 5'  # Dashed line
    ).add_to(m)
    
    print(f"📦 {name}: {data['points']} points (RECTANGLE)")

# Add legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 300px; height: 140px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; border-radius: 5px; padding: 10px">
<h4 style="margin-top:0">Polygon Detail Comparison</h4>
<p><span style="color:#00ff00;">━━━</span> <b>Detailed polygons</b> (50-900+ points)<br>
   Accurate outlines from OpenStreetMap</p>
<p><span style="color:#ff0000;">- - -</span> <b>Simple rectangles</b> (4-5 points)<br>
   Basic approximations</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Add layer control
folium.LayerControl().add_to(m)

# Save map
output_file = 'static/detailed_vs_simple_polygons.html'
m.save(output_file)

print("\n" + "=" * 70)
print(f"✅ Preview map saved to: {output_file}")
print("=" * 70)
print("\nCOMPARISON:")
print("  🟢 GREEN = Detailed polygons (accurate outlines)")
print("  🔴 RED DASHED = Simple rectangles (basic approximations)")
print()
print("You can see the difference - detailed polygons follow the")
print("actual shape of the features, just like your reference map!")
print("=" * 70)


