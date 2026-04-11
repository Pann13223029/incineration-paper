"""
00_probe_estat_facility_data.py
================================
PURPOSE: Determine whether facility-level incinerator data is available
from e-Stat (Japan's government statistics portal) in downloadable form.

This is the thesis's load-bearing question:
- If YES → facility-level panel design
- If NO  → pivot to prefecture-level aggregates

The MOE General Waste Treatment Survey (一般廃棄物処理事業実態調査)
is on e-Stat under survey ID 00650101. This script:
1. Queries the e-Stat API for available tables
2. Filters for facility/incinerator-related tables
3. Downloads a sample to inspect variables
4. Reports what's available

Requires: ESTAT_APP_ID environment variable (free registration at e-stat.go.jp)
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import time

# --- Config ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'raw')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

APP_ID = os.environ.get('ESTAT_APP_ID')
if not APP_ID:
    print("ERROR: Set ESTAT_APP_ID environment variable.")
    print("Register for free at: https://www.e-stat.go.jp/")
    sys.exit(1)

BASE_URL = "https://api.e-stat.go.jp/rest/3.0/app/json"

# --- Step 1: List all tables for the General Waste Survey ---
print("=" * 60)
print("Step 1: Querying e-Stat for General Waste Survey tables...")
print("Survey ID: 00650101 (一般廃棄物処理事業実態調査)")
print("=" * 60)

params = urllib.parse.urlencode({
    'appId': APP_ID,
    'statsCode': '00650101',
    'limit': 100,
})

url = f"{BASE_URL}/getStatsList?{params}"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

if 'GET_STATS_LIST' not in data:
    print("ERROR: Unexpected API response.")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
    sys.exit(1)

result = data['GET_STATS_LIST']
if 'DATALIST_INF' not in result:
    print("No data lists found.")
    sys.exit(1)

tables = result['DATALIST_INF'].get('TABLE_INF', [])
if not isinstance(tables, list):
    tables = [tables]

print(f"\nFound {len(tables)} tables total.\n")

# --- Step 2: Filter for facility-related tables ---
print("=" * 60)
print("Step 2: Filtering for facility/incinerator tables...")
print("=" * 60)

# Keywords that suggest facility-level data
FACILITY_KEYWORDS = [
    '施設', '焼却', 'しせつ', '処理施設', '発電', 'エネルギー',
    'facility', 'incinerat', 'plant', 'energy'
]

facility_tables = []
all_tables_summary = []

for t in tables:
    table_id = t.get('@id', 'N/A')
    title = t.get('TITLE', {})
    if isinstance(title, dict):
        title_text = title.get('$', str(title))
    else:
        title_text = str(title)

    survey_date = t.get('SURVEY_DATE', 'N/A')

    summary = {
        'id': table_id,
        'title': title_text,
        'date': survey_date,
    }
    all_tables_summary.append(summary)

    # Check if facility-related
    title_lower = title_text.lower()
    if any(kw in title_lower for kw in FACILITY_KEYWORDS):
        facility_tables.append(summary)
        print(f"  MATCH: [{table_id}] {title_text} ({survey_date})")

print(f"\n{len(facility_tables)} facility-related tables found out of {len(tables)} total.")

# Save full table list for reference
table_list_path = os.path.join(OUTPUT_DIR, 'estat_waste_survey_tables.json')
with open(table_list_path, 'w', encoding='utf-8') as f:
    json.dump(all_tables_summary, f, indent=2, ensure_ascii=False)
print(f"\nFull table list saved to: {table_list_path}")

# --- Step 3: Download a sample facility table ---
if facility_tables:
    print("\n" + "=" * 60)
    print("Step 3: Downloading sample facility table...")
    print("=" * 60)

    sample = facility_tables[0]
    sample_id = sample['id']
    print(f"  Table: [{sample_id}] {sample['title']}")

    time.sleep(0.5)  # rate limit

    params = urllib.parse.urlencode({
        'appId': APP_ID,
        'statsDataId': sample_id,
        'limit': 50,  # just a sample
    })

    url = f"{BASE_URL}/getStatsData?{params}"
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req) as resp:
            sample_data = json.loads(resp.read().decode('utf-8'))

        # Save raw sample
        sample_path = os.path.join(RAW_DIR, f'estat_sample_{sample_id}.json')
        with open(sample_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        print(f"  Sample saved to: {sample_path}")

        # Extract and display variable metadata
        stat_data = sample_data.get('GET_STATS_DATA', {})
        class_inf = stat_data.get('STATISTICAL_DATA', {}).get('CLASS_INF', {})
        class_obj = class_inf.get('CLASS_OBJ', [])

        if not isinstance(class_obj, list):
            class_obj = [class_obj]

        print("\n  Variables (CLASS_OBJ) in this table:")
        for cls in class_obj:
            cls_id = cls.get('@id', 'N/A')
            cls_name = cls.get('@name', 'N/A')
            classes = cls.get('CLASS', [])
            if not isinstance(classes, list):
                classes = [classes]
            n_cats = len(classes)
            sample_cats = [c.get('@name', '?') for c in classes[:5]]
            print(f"    {cls_id}: {cls_name} ({n_cats} categories)")
            print(f"      Examples: {', '.join(sample_cats)}")

        # Check for facility-level identifiers
        print("\n  Checking for facility-level granularity...")
        all_class_names = ' '.join([
            cls.get('@name', '') for cls in class_obj
        ] + [
            c.get('@name', '')
            for cls in class_obj
            for c in (cls.get('CLASS', []) if isinstance(cls.get('CLASS', []), list) else [cls.get('CLASS', {})])
        ])

        if any(kw in all_class_names for kw in ['施設', '焼却', 'プラント', 'facility']):
            print("  >>> FACILITY-LEVEL DATA DETECTED <<<")
        else:
            print("  >>> Data appears to be MUNICIPALITY or PREFECTURE level <<<")
            print("  (May need to check more tables)")

    except Exception as e:
        print(f"  ERROR downloading sample: {e}")
else:
    print("\nNo facility-related tables found. Will need to check MOE direct downloads.")

# --- Step 4: Also list ALL table titles for manual review ---
print("\n" + "=" * 60)
print("Step 4: All available tables (for manual review)")
print("=" * 60)
for t in all_tables_summary[:50]:  # first 50
    print(f"  [{t['id']}] {t['title']} ({t['date']})")
if len(all_tables_summary) > 50:
    print(f"  ... and {len(all_tables_summary) - 50} more (see JSON output)")

print("\n" + "=" * 60)
print("DONE. Review output above and estat_waste_survey_tables.json")
print("=" * 60)
