#!/usr/bin/env python3
"""
Tool to help digitize detailed polygons from nautical charts.

This script shows how to:
1. Load a georeferenced nautical chart image
2. Let you trace polygons by clicking points
3. Export coordinates for use in Folium
"""

import folium
from folium import plugins
import json

def create_digitizing_map(center_lat=12.0, center_lon=115.0, zoom=6):
    """
    Create an interactive map for digitizing polygons.
    
    Usage:
    1. Click points around the feature boundary
    2. Copy the coordinates from browser console
    3. Use them in your patrol map
    """
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    
    # Add satellite imagery for reference (helps trace features)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add nautical charts layer from NOAA
    folium.TileLayer(
        tiles='https://gis.ngdc.noaa.gov/arcgis/rest/services/web_mercator/gebco_2020/MapServer/tile/{z}/{y}/{x}',
        attr='GEBCO/NOAA',
        name='Bathymetry',
        overlay=True,
        control=True
    ).add_to(m)
    
    # Add drawing tools
    draw = plugins.Draw(
        export=True,
        filename='digitized_features.geojson',
        position='topleft',
        draw_options={
            'polyline': False,
            'rectangle': False,
            'circle': False,
            'circlemarker': False,
            'marker': False,
            'polygon': {
                'allowIntersection': False,
                'drawError': {
                    'color': '#e1e100',
                    'message': '<strong>Error:</strong> shape edges cannot cross!'
                },
                'shapeOptions': {
                    'color': '#d4a373',
                    'weight': 2,
                    'fillOpacity': 0.3
                }
            }
        }
    )
    draw.add_to(m)
    
    # Add coordinate display on click
    m.get_root().html.add_child(folium.Element("""
    <script>
    var coordinates = [];
    var currentPolygon = null;
    
    function addPoint(lat, lng) {
        coordinates.push([lat, lng]);
        console.log('Point added:', lat.toFixed(6), lng.toFixed(6));
        console.log('Current polygon:', JSON.stringify(coordinates));
    }
    
    function clearPolygon() {
        coordinates = [];
        console.log('Polygon cleared');
    }
    
    function finishPolygon() {
        console.log('='.repeat(70));
        console.log('FINISHED POLYGON - Copy these coordinates:');
        console.log('Python format (lat, lon):');
        var python_coords = coordinates.map(c => '    (' + c[0].toFixed(6) + ', ' + c[1].toFixed(6) + ')').join(',\\n');
        console.log('[\\n' + python_coords + '\\n]');
        console.log('='.repeat(70));
        clearPolygon();
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'c' || e.key === 'C') {
            clearPolygon();
        } else if (e.key === 'f' || e.key === 'F') {
            finishPolygon();
        }
    });
    
    console.log('DIGITIZING TOOL READY');
    console.log('Instructions:');
    console.log('1. Use polygon tool to trace feature');
    console.log('2. Click points around boundary');
    console.log('3. Double-click to finish polygon');
    console.log('4. Check console for coordinates');
    console.log('5. Press C to clear, F to finish');
    </script>
    """))
    
    # Add some reference points for known features
    reference_points = {
        'Macclesfield Bank (center)': (16.0, 114.8),
        'Dangerous Ground (center)': (9.5, 115.0),
        'Paracel Islands (center)': (16.5, 112.0),
        'Reed Bank (center)': (11.0, 116.5)
    }
    
    for name, (lat, lon) in reference_points.items():
        folium.Marker(
            location=[lat, lon],
            popup=name,
            icon=folium.Icon(color='red', icon='info-sign'),
            tooltip=name
        ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    return m

if __name__ == '__main__':
    # Create digitizing map
    m = create_digitizing_map()
    
    output_file = 'static/digitize_polygons.html'
    m.save(output_file)
    
    print("✅ Digitizing map created!")
    print(f"📍 Open: {output_file}")
    print()
    print("INSTRUCTIONS:")
    print("1. Open the HTML file in your browser")
    print("2. Use the polygon tool (square icon on left)")
    print("3. Click to trace around Macclesfield Bank, Dangerous Ground, etc.")
    print("4. Double-click to finish polygon")
    print("5. Open browser console (F12) to see coordinates")
    print("6. Copy coordinates and paste into generate_patrol_map.py")
    print()
    print("TIP: Switch to 'Satellite' layer to see features clearly!")


