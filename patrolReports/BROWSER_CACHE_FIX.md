# 🔧 BROWSER CACHE ISSUE - How to Fix

## Problem

The precise depth code is **deployed to production**, but your browser is showing the old cached version with depth ranges.

## Verification

✅ Production file contains the new code (confirmed):
```bash
grep "getPreciseDepth" /var/www/html/codpatrols/static/patrol_tracks.html
# Returns: async function getPreciseDepth(lat, lon)
```

✅ File timestamp is recent: Dec 27 15:13

## Solution: Clear Browser Cache

### Method 1: Hard Refresh (Fastest)

**Windows/Linux:**
1. Open the patrol map page
2. Press `Ctrl + Shift + R` or `Ctrl + F5`

**Mac:**
1. Open the patrol map page
2. Press `Cmd + Shift + R`

This forces the browser to reload everything from the server.

### Method 2: Clear Cache (Most Thorough)

**Chrome/Edge:**
1. Press `F12` to open Developer Tools
2. Right-click the refresh button (↻)
3. Select "Empty Cache and Hard Reload"

**Firefox:**
1. Press `Ctrl + Shift + Delete` (Windows) or `Cmd + Shift + Delete` (Mac)
2. Select "Cached Web Content"
3. Click "Clear Now"
4. Reload the page

**Safari:**
1. `Safari` → `Preferences` → `Advanced`
2. Check "Show Develop menu in menu bar"
3. `Develop` → `Empty Caches`
4. Reload the page

### Method 3: Incognito/Private Mode (Quick Test)

Open the patrol map in an incognito/private browsing window:
- **Chrome/Edge**: `Ctrl + Shift + N`
- **Firefox**: `Ctrl + Shift + P`
- **Safari**: `Cmd + Shift + N`

This uses no cache and will show you the current production version.

### Method 4: Add Cache-Busting Parameter

Add a version parameter to the URL:
```
https://codpatrols.com/static/patrol_tracks.html?v=20241227
```

The `?v=...` forces browser to treat it as a new file.

## Verify It's Working

After clearing cache:

1. **Click** on ocean
2. **See** "⏳ Fetching precise depth..." (loading message)
3. **Wait** ~1 second
4. **Get** precise depth like "287 m" (not a range like "100-500 m")
5. **Look for** "(GEBCO bathymetry data)" at bottom of popup

## If Still Not Working

### Check 1: View Page Source
1. Right-click page → "View Page Source"
2. Press `Ctrl + F` to search
3. Search for: `getPreciseDepth`
4. If found → Cache issue (clear cache harder)
5. If not found → Not deployed (run deploy script)

### Check 2: Check Browser Console
1. Press `F12` to open Developer Tools
2. Click "Console" tab
3. Click on ocean
4. Look for any error messages

### Check 3: Check Network Tab
1. Press `F12` to open Developer Tools
2. Click "Network" tab
3. Reload page
4. Look for `patrol_tracks.html` request
5. Check if it says "(from cache)" or "200" status

## Web Server Cache

If your web server has caching enabled (Apache mod_cache, nginx proxy_cache, etc.), you may need to clear that too:

### Apache:
```bash
sudo systemctl reload apache2
```

### Nginx:
```bash
sudo systemctl reload nginx
```

### Check current cache headers:
```bash
curl -I https://codpatrols.com/static/patrol_tracks.html
```

Look for `Cache-Control` and `ETag` headers.

## For Users Visiting Your Site

If you want to ensure ALL users get the new version immediately, you can:

### Option 1: Add Cache-Control Headers

Add to Apache config:
```apache
<Location /static/patrol_tracks.html>
    Header set Cache-Control "no-cache, must-revalidate"
</Location>
```

### Option 2: Version the Filename

Rename file to include version:
```
patrol_tracks_v2.html
```

Update links to point to new filename.

### Option 3: Add ETag/Last-Modified

The server already should send these, but you can verify:
```bash
curl -I https://codpatrols.com/static/patrol_tracks.html
```

## Quick Test Command

Run this from your terminal to see what version the server is serving:

```bash
curl -s https://codpatrols.com/static/patrol_tracks.html | grep -o "getPreciseDepth" | head -1
```

If it returns "getPreciseDepth" → New version is deployed
If it returns nothing → Old version still deployed

## Summary

**The issue is browser cache, not deployment.**

✅ **Fix**: Hard refresh with `Ctrl + Shift + R` or `Ctrl + F5`
✅ **Verify**: Click ocean, see "⏳ Fetching..." then precise depth
✅ **Help others**: They'll need to hard refresh too, or wait for browser cache to expire

---

**Status**: Code is deployed, just need to clear browser cache!
**Quick Fix**: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)


