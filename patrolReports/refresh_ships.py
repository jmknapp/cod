#!/usr/bin/env python3
"""
Refresh the ship_contacts table from the Excel file.

Usage:
    python refresh_ships.py
"""

import mysql.connector
import pandas as pd
import os

EXCEL_FILE = os.path.join(os.path.dirname(__file__), 'Cod_ship_contacts.xlsx')

def safe_int(val):
    if pd.isna(val) or val == '' or (isinstance(val, str) and val.strip() == ''):
        return None
    return int(float(val))

def safe_float(val):
    if pd.isna(val) or val == '' or (isinstance(val, str) and val.strip() == ''):
        return None
    return float(val)

def safe_str(val):
    if pd.isna(val) or val == '' or (isinstance(val, str) and val.strip() == ''):
        return None
    return str(val).strip()

def refresh_ships():
    # Read the Excel file
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: Excel file not found: {EXCEL_FILE}")
        return False
    
    df = pd.read_excel(EXCEL_FILE)
    print(f"Read {df.shape[0]} rows from {os.path.basename(EXCEL_FILE)}")

    # Connect to MySQL
    from db_config import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear and reload
    cursor.execute("DELETE FROM ship_contacts")

    insert_sql = """
        INSERT INTO ship_contacts 
        (patrol, contact_no, observation_time, timezone, observation_date, 
         latitude_deg, latitude_min, latitude_hemisphere,
         longitude_deg, longitude_min, longitude_hemisphere,
         latitude, longitude, ship_type, range_yards, course, speed, method, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    rows_inserted = 0
    for idx, row in df.iterrows():
        # Skip rows with missing patrol number (empty rows)
        if pd.isna(row['patrol']) or safe_int(row['patrol']) is None:
            continue
            
        lat_deg = safe_int(row['latitude deg'])
        lat_min = safe_int(row['latitude min'])
        lon_deg = safe_int(row['longitude deg'])
        lon_min = safe_int(row['longitude min'])
        
        # Get hemispheres from file or default
        lat_hem = 'N'
        lon_hem = 'E'
        for col in df.columns:
            if 'latitude' in col.lower() and 'hemisphere' in col.lower():
                val = safe_str(row[col])
                if val:
                    lat_hem = val.upper()[0]
            if 'longitude' in col.lower() and 'hemisphere' in col.lower():
                val = safe_str(row[col])
                if val:
                    lon_hem = val.upper()[0]
        
        # Calculate decimal lat/lon with hemisphere
        latitude = None
        longitude = None
        if lat_deg is not None and lat_min is not None:
            latitude = lat_deg + lat_min / 60.0
            if lat_hem == 'S':
                latitude = -latitude
        if lon_deg is not None and lon_min is not None:
            longitude = lon_deg + lon_min / 60.0
            if lon_hem == 'W':
                longitude = -longitude
        
        obs_time = None
        if pd.notna(row['observation time']):
            try:
                # Convert military time (e.g., 1200) to HH:MM format
                time_val = str(int(float(row['observation time']))).zfill(4)
                obs_time = f"{time_val[:2]}:{time_val[2:]}"
            except:
                obs_time = safe_str(row['observation time'])
        
        obs_date = row['observation date'].date() if pd.notna(row['observation date']) else None
        
        # Contact can be string like "SC1", "J1", "MS1" or numeric
        contact_val = row['contact']
        if pd.notna(contact_val):
            contact_str = str(contact_val).strip()
            # Remove ".0" if it's a float converted to string
            if contact_str.endswith('.0'):
                contact_str = contact_str[:-2]
        else:
            contact_str = None
        
        # Course can be numeric (170) or with suffix (170T) or text (Southerly)
        # Extract numeric portion if possible
        course_val = row['course']
        course_int = None
        if pd.notna(course_val):
            course_str = str(course_val).strip()
            # Try to extract leading digits
            import re
            match = re.match(r'^(\d+)', course_str)
            if match:
                course_int = int(match.group(1))
        
        values = (
            safe_int(row['patrol']),
            contact_str,
            obs_time,
            safe_str(row['timezone']),
            obs_date,
            lat_deg, lat_min, lat_hem,
            lon_deg, lon_min, lon_hem,
            latitude, longitude,
            safe_str(row['type']),
            safe_int(row['range']),
            course_int,
            safe_float(row['speed']),
            safe_str(row['method']),
            safe_str(row['remarks'])
        )
        
        cursor.execute(insert_sql, values)
        rows_inserted += 1

    conn.commit()

    # Summary
    cursor.execute("SELECT patrol, COUNT(*) FROM ship_contacts GROUP BY patrol ORDER BY patrol")
    print(f"\nInserted {rows_inserted} total rows:")
    for row in cursor.fetchall():
        print(f"  Patrol {row[0]}: {row[1]} contacts")

    cursor.close()
    conn.close()
    print("\nDone!")
    return True

if __name__ == '__main__':
    refresh_ships()

