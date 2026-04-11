"""
01_download_facility_data.py
============================
Download incineration facility Excel files from the MOE General Waste
Treatment Survey for FY2005-2024 (h17 to r6).

Each file contains facility-level data for every incinerator in Japan:
- Facility ID, name, location (prefecture + municipality)
- Annual throughput (t/year), capacity (t/day), number of furnaces
- Year started operation
- Power generation capacity (kW), efficiency (%), actual output (MWh)
- Heat utilization (MJ), electricity sold (MWh), revenue (yen)
- Waste composition (paper, plastic, wood, food, etc.)
- Heating value (kJ/kg)

URL pattern:
  https://www.env.go.jp/recycle/waste_tech/ippan/{era_code}/data/seibi/facility/01.{ext}

Older years (h17-h30) use .xls; newer years (r1-r6) use .xlsx.
Some years may use the other extension — the script tries both.
"""

import os
import sys
import time
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'raw', 'facility_annual')
os.makedirs(RAW_DIR, exist_ok=True)

BASE_URL = "https://www.env.go.jp/recycle/waste_tech/ippan"

# FY2005 = h17, FY2006 = h18, ..., FY2018 = h30, FY2019 = r1, ..., FY2024 = r6
YEARS = {
    2005: 'h17', 2006: 'h18', 2007: 'h19', 2008: 'h20',
    2009: 'h21', 2010: 'h22', 2011: 'h23', 2012: 'h24',
    2013: 'h25', 2014: 'h26', 2015: 'h27', 2016: 'h28',
    2017: 'h29', 2018: 'h30',
    2019: 'r1', 2020: 'r2', 2021: 'r3', 2022: 'r4',
    2023: 'r5', 2024: 'r6',
}


def download_file(url, dest):
    """Download a file, return True on success."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (research; APU thesis)'
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            content_type = resp.headers.get('Content-Type', '')
            data = resp.read()

            # Check if we got a 404 HTML page instead of a real file
            if b'<!DOCTYPE html>' in data[:500] and b'404' in data[:2000]:
                return False
            if len(data) < 5000:  # real facility files are >30KB
                # Might be an error page
                if b'<html' in data[:500].lower():
                    return False

            with open(dest, 'wb') as f:
                f.write(data)
            return True
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        return False


def main():
    print("=" * 60)
    print("Downloading MOE Incineration Facility Data")
    print(f"Years: FY{min(YEARS.keys())} to FY{max(YEARS.keys())}")
    print(f"Output: {os.path.abspath(RAW_DIR)}")
    print("=" * 60)

    results = {}

    for fy, era_code in sorted(YEARS.items()):
        # Try .xlsx first (newer format), then .xls
        success = False
        for ext in ['xlsx', 'xls']:
            url = f"{BASE_URL}/{era_code}/data/seibi/facility/01.{ext}"
            dest = os.path.join(RAW_DIR, f"fy{fy}_incineration.{ext}")

            print(f"  FY{fy} ({era_code}): trying .{ext}...", end=" ", flush=True)

            if download_file(url, dest):
                size_kb = os.path.getsize(dest) / 1024
                print(f"OK ({size_kb:.0f} KB)")
                results[fy] = {'status': 'OK', 'file': dest, 'ext': ext, 'size_kb': size_kb}
                success = True
                break
            else:
                print("not found")
                # Clean up failed download
                if os.path.exists(dest):
                    os.remove(dest)

            time.sleep(0.5)  # rate limit

        if not success:
            print(f"  FY{fy} ({era_code}): FAILED (neither .xlsx nor .xls found)")
            results[fy] = {'status': 'FAILED'}

        time.sleep(0.3)  # rate limit between years

    # --- Summary ---
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)

    ok_count = sum(1 for r in results.values() if r['status'] == 'OK')
    fail_count = sum(1 for r in results.values() if r['status'] == 'FAILED')

    for fy in sorted(results.keys()):
        r = results[fy]
        if r['status'] == 'OK':
            print(f"  FY{fy}: OK ({r['ext']}, {r['size_kb']:.0f} KB)")
        else:
            print(f"  FY{fy}: FAILED")

    print(f"\nTotal: {ok_count} downloaded, {fail_count} failed out of {len(YEARS)} years")

    if ok_count >= 10:
        print("\nSufficient data for panel analysis. Proceed to parsing.")
    elif ok_count >= 5:
        print("\nPartial data. May need to adjust panel window.")
    else:
        print("\nInsufficient data. Check URLs manually or consider prefecture-level fallback.")


if __name__ == '__main__':
    main()
