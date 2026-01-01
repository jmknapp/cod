#!/usr/bin/env python3
"""
Fetch detailed polygons from OpenStreetMap for South China Sea features.

OpenStreetMap has detailed outlines for many nautical features.
"""

import requests
import json
import time

def query_overpass(feature_name, bbox=None):
    """
    Query OpenStreetMap Overpass API for a named feature.
    
    Args:
        feature_name: Name of the feature (e.g., "Macclesfield Bank")
        bbox: Optional bounding box [south, west, north, east]
    
    Returns:
        GeoJSON-like structure with coordinates
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Build bounding box string if provided
    bbox_str = ""
    if bbox:
        bbox_str = f"({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]})"
    
    # Query for ways and relations with this name
    query = f"""
    [out:json][timeout:25];
    (
      way["name"="{feature_name}"]{bbox_str};
      way["name:en"="{feature_name}"]{bbox_str};
      relation["name"="{feature_name}"]{bbox_str};
      relation["name:en"="{feature_name}"]{bbox_str};
      
      // Also search for reef, bank, shoal tags
      way["seamark:type"="reef"]["name"="{feature_name}"]{bbox_str};
      way["seamark:type"="bank"]["name"="{feature_name}"]{bbox_str};
      way["natural"="reef"]["name"="{feature_name}"]{bbox_str};
    );
    out geom;
    >;
    out skel qt;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  ❌ Error fetching {feature_name}: {e}")
        return None

def extract_coordinates(osm_data):
    """Extract coordinates from OSM data"""
    if not osm_data or 'elements' not in osm_data:
        return None
    
    for element in osm_data['elements']:
        if element['type'] == 'way' and 'geometry' in element:
            # Extract coordinates from way
            coords = [(point['lat'], point['lon']) for point in element['geometry']]
            return coords
        elif element['type'] == 'relation':
            # For relations, need to piece together member ways
            # This is more complex - simplified version
            pass
    
    return None

def search_south_china_sea_features():
    """Search for detailed polygons of SCS features"""
    
    features_to_search = [
        {
            'name': 'Macclesfield Bank',
            'alt_names': ['Zhongsha Islands', 'Macclesfield'],
            'bbox': [15.0, 113.5, 17.0, 116.0]  # [south, west, north, east]
        },
        {
            'name': 'Dangerous Ground',
            'alt_names': ['Spratly Islands', 'Nansha Islands'],
            'bbox': [7.0, 112.0, 12.0, 118.0]
        },
        {
            'name': 'Paracel Islands',
            'alt_names': ['Xisha Islands', 'Hoang Sa'],
            'bbox': [15.5, 110.5, 17.5, 113.0]
        },
        {
            'name': 'Scarborough Shoal',
            'alt_names': ['Huangyan Island', 'Scarborough Reef'],
            'bbox': [15.0, 117.5, 15.3, 118.0]
        },
        {
            'name': 'Reed Bank',
            'alt_names': ['Recto Bank', 'Reed Tablemount'],
            'bbox': [10.0, 115.5, 12.0, 118.0]
        }
    ]
    
    results = {}
    
    print("🔍 Searching OpenStreetMap for detailed polygons...")
    print("=" * 70)
    
    for feature in features_to_search:
        print(f"\n📍 Searching for: {feature['name']}")
        
        # Try main name
        data = query_overpass(feature['name'], feature['bbox'])
        coords = extract_coordinates(data) if data else None
        
        # Try alternative names if main name didn't work
        if not coords:
            for alt_name in feature['alt_names']:
                print(f"  Trying alternative name: {alt_name}")
                data = query_overpass(alt_name, feature['bbox'])
                coords = extract_coordinates(data) if data else None
                if coords:
                    break
                time.sleep(1)  # Be nice to Overpass API
        
        if coords:
            results[feature['name']] = coords
            print(f"  ✅ Found {len(coords)} coordinate points")
        else:
            print(f"  ⚠️  No detailed polygon found (will need manual digitization)")
        
        time.sleep(2)  # Rate limiting
    
    return results

def save_detailed_geojson(results, output_file='static/geojson/detailed_features.json'):
    """Save results as GeoJSON"""
    
    features = []
    for name, coords in results.items():
        # Convert to GeoJSON format [lon, lat]
        geojson_coords = [[[lon, lat] for lat, lon in coords]]
        
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': geojson_coords
            },
            'properties': {
                'name': name,
                'source': 'OpenStreetMap',
                'detail_level': 'high'
            }
        })
    
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"\n✅ Saved to: {output_file}")

def print_folium_code(results):
    """Print ready-to-use Folium code"""
    
    print("\n" + "=" * 70)
    print("FOLIUM CODE (copy and paste):")
    print("=" * 70)
    
    for name, coords in results.items():
        var_name = name.lower().replace(' ', '_').replace('-', '_')
        
        print(f"\n# {name}")
        print(f"{var_name}_coords = [")
        for lat, lon in coords[:10]:  # Show first 10 points
            print(f"    ({lat:.6f}, {lon:.6f}),")
        if len(coords) > 10:
            print(f"    # ... {len(coords) - 10} more points ...")
        print("]")
        
        print(f"""
folium.Polygon(
    locations={var_name}_coords,
    color='#d4a373',
    weight=2,
    fill=True,
    fill_color='#d4a373',
    fill_opacity=0.3,
    popup='<b>{name}</b>',
    tooltip='{name}'
).add_to(m)
""")

if __name__ == '__main__':
    print("DETAILED POLYGON FETCHER")
    print("Queries OpenStreetMap for accurate feature outlines")
    print()
    
    # Search for features
    results = search_south_china_sea_features()
    
    if results:
        # Save as GeoJSON
        save_detailed_geojson(results)
        
        # Print Folium code
        print_folium_code(results)
        
        print("\n✅ Complete!")
        print(f"   Found {len(results)} features with detailed polygons")
    else:
        print("\n⚠️  No features found in OpenStreetMap")
        print("   Recommendation: Use manual digitization tool instead")
        print("   Run: python3 digitize_nautical_polygons.py")


