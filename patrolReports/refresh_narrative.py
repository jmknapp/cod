#!/usr/bin/env python3
"""
Refresh narrative_page_index table from Excel file.
Maps patrol report pages to dates/times for linking search results to correct pages.
"""

import pandas as pd
from db_config import get_db_connection

def safe_int(val):
    """Safely convert to int, return None if not possible."""
    if pd.isna(val):
        return None
    try:
        return int(float(val))
    except:
        return None

def safe_str(val):
    """Safely convert to string, return None if empty."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    return s if s else None

def refresh_narrative():
    """Load narrative page index from Excel into database."""
    
    # Read Excel file
    xlsx_file = 'narrativePageIndexCod.xlsx'
    df = pd.read_excel(xlsx_file)
    print(f"Read {len(df)} rows from {xlsx_file}")
    print(f"Columns: {list(df.columns)}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM narrative_page_index")
    
    insert_sql = """
        INSERT INTO narrative_page_index 
        (patrol, page, observation_date, observation_time)
        VALUES (%s, %s, %s, %s)
    """
    
    rows_inserted = 0
    for idx, row in df.iterrows():
        # Skip rows with missing patrol number
        patrol = safe_int(row.get('patrol') or row.get('Patrol'))
        if patrol is None:
            continue
        
        page = safe_int(row.get('page') or row.get('Page'))
        if page is None:
            continue
        
        # Get observation date
        obs_date = None
        date_col = None
        for col in ['observation_date', 'observation date', 'date', 'Date']:
            if col in row and pd.notna(row[col]):
                date_col = col
                break
        
        if date_col:
            try:
                obs_date = pd.to_datetime(row[date_col]).date()
            except:
                obs_date = None
        
        if obs_date is None:
            continue
        
        # Get observation time (stored as HHMM string)
        obs_time = None
        time_col = None
        for col in ['observation_time', 'observation time', 'time', 'Time']:
            if col in row and pd.notna(row[col]):
                time_col = col
                break
        
        if time_col:
            try:
                time_val = str(int(float(row[time_col]))).zfill(4)
                obs_time = time_val
            except:
                obs_time = safe_str(row[time_col])
        
        values = (patrol, page, obs_date, obs_time)
        
        cursor.execute(insert_sql, values)
        rows_inserted += 1
    
    conn.commit()
    
    # Summary
    cursor.execute("SELECT patrol, COUNT(*) FROM narrative_page_index GROUP BY patrol ORDER BY patrol")
    print(f"\nInserted {rows_inserted} total rows:")
    for row in cursor.fetchall():
        print(f"  Patrol {row[0]}: {row[1]} entries")
    
    cursor.close()
    conn.close()
    print("\nDone!")
    return True

if __name__ == '__main__':
    refresh_narrative()

