"""
02_parse_facility_panel.py
==========================
Parse all 20 years of MOE incineration facility Excel files into a single
panel dataset with standardized column names.

Uses AUTO-DETECTION of column positions by searching for Japanese header
keywords, eliminating the need for hardcoded per-year column mappings.
Column positions shift across years (43 to 100 columns), but header text
is consistent enough for reliable matching.
"""

import os
import sys
import pandas as pd
import numpy as np
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'raw', 'facility_annual')
PROCESSED_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'processed')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Header keywords for auto-detection
# Each entry: (standardized_name, [keywords_to_search], search_rows)
COLUMN_DEFS = [
    ('prefecture',           ['都道府県名', '都道府県コード'],    ),
    ('muni_code',            ['地方公共団体コード'],              ),
    ('facility_code',        ['施設コード'],                      ),
    ('facility_name',        ['施設名称'],                        ),
    ('throughput_t_year',    ['年間処理量'],                      ),
    ('capacity_t_day',       ['処理能力', '施設全体の処理能力'],  ),
    ('n_furnaces',           ['炉数'],                            ),
    ('year_started',         ['使用開始年度'],                    ),
    ('heat_util_status',     ['余熱利用の状況'],                  ),
    ('power_capacity_kw',    ['発電能力'],                        ),
    ('power_efficiency_pct', ['発電効率'],                        ),
    ('power_generated_mwh',  ['総発電量'],                        ),
    ('power_sold_mwh',       ['売電量', '余剰電力'],             ),
    ('heating_value_kj_kg',  ['低発熱量', '低位発熱量'],         ),
    ('furnace_type',         ['処理方式'],                        ),
    ('operation_mode',       ['炉型式'],                          ),
    ('waste_type',           ['焼却対象廃棄物', '処理対象廃棄物'],),
    ('facility_type',        ['施設の種類'],                      ),
    ('sell_revenue_yen',     ['売電収入'],                        ),
]


def normalize(s):
    """Normalize Japanese text for matching (NFKC + strip)."""
    if pd.isna(s):
        return ''
    return unicodedata.normalize('NFKC', str(s)).strip()


def find_column(df_header, keywords, max_rows=6):
    """Find the column index containing any of the keywords in the header rows."""
    for r in range(min(max_rows, df_header.shape[0])):
        for c in range(df_header.shape[1]):
            val = normalize(df_header.iloc[r, c])
            if any(kw in val for kw in keywords):
                return c
    return None


def find_data_start(df_raw):
    """Find the first row that looks like data (not headers/titles).
    FY2005-2006: data starts at row 1-2 (headers in row 0)
    FY2007+: data starts at row 6 (title + multi-row headers in rows 0-5)
    """
    # Check if row 0 contains '都道府県' (direct header = old format)
    row0_text = ' '.join([normalize(df_raw.iloc[0, c]) for c in range(min(10, df_raw.shape[1]))])
    if '都道府県コード' in row0_text or '都道府県名' in row0_text:
        # Old format: row 0 is headers
        # Check if row 1 is also header (sub-headers) or data
        row1_val = normalize(df_raw.iloc[1, 0])
        if row1_val and any(c.isdigit() for c in row1_val):
            return 1  # row 1 is data (pure numeric prefecture code)
        else:
            return 2  # row 1 is sub-header
    else:
        # New format: title at row 0, headers at rows 1-5, data at row 6
        return 6


def parse_year(fy):
    """Parse a single fiscal year's facility file."""
    for ext in ['xlsx', 'xls']:
        fpath = os.path.join(RAW_DIR, f'fy{fy}_incineration.{ext}')
        if os.path.exists(fpath):
            break
    else:
        return None

    engine = 'openpyxl' if fpath.endswith('.xlsx') else 'xlrd'
    df_raw = pd.read_excel(fpath, sheet_name=0, header=None, engine=engine)

    # Auto-detect column positions
    col_map = {}
    for col_name, keywords in COLUMN_DEFS:
        idx = find_column(df_raw, keywords)
        if idx is not None:
            col_map[col_name] = idx

    # Find data start
    data_start = find_data_start(df_raw)
    df_data = df_raw.iloc[data_start:].copy().reset_index(drop=True)

    # For FY2005-2006, prefecture is in col 1 (都道府県名) but auto-detect
    # may have found col 0 (都道府県コード). Use the name column.
    # Check if col_map['prefecture'] points to a code or a name
    if 'prefecture' in col_map:
        sample_val = normalize(df_data.iloc[0, col_map['prefecture']])
        if sample_val and sample_val.isdigit():
            # This is a code column, look for the name column (usually +1)
            name_col = col_map['prefecture'] + 1
            if name_col < df_data.shape[1]:
                sample_name = normalize(df_data.iloc[0, name_col])
                if sample_name and not sample_name.isdigit():
                    col_map['prefecture'] = name_col

    # Drop rows where prefecture is empty (footers/summaries)
    if 'prefecture' in col_map:
        pref_col = col_map['prefecture']
        df_data = df_data[df_data.iloc[:, pref_col].apply(
            lambda x: pd.notna(x) and normalize(x) != ''
        )].reset_index(drop=True)

    # Extract columns into standardized DataFrame
    result = pd.DataFrame()

    for col_name, col_idx in col_map.items():
        if col_idx < df_data.shape[1]:
            result[col_name] = df_data.iloc[:, col_idx].values
        else:
            result[col_name] = np.nan

    # Set fiscal year AFTER columns are populated (avoids broadcast bug)
    result['fiscal_year'] = fy

    # Convert numeric columns
    numeric_cols = [
        'throughput_t_year', 'capacity_t_day', 'n_furnaces', 'year_started',
        'power_capacity_kw', 'power_efficiency_pct', 'power_generated_mwh',
        'power_sold_mwh', 'sell_revenue_yen', 'heating_value_kj_kg',
    ]
    for col in numeric_cols:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce')

    # FY2005-2006 heating value may be in kcal/kg (values ~1000-3000)
    # FY2007+ uses kJ/kg (values ~4000-12000)
    # Auto-detect by checking median value
    if 'heating_value_kj_kg' in result.columns:
        median_hv = result['heating_value_kj_kg'].median()
        if pd.notna(median_hv) and median_hv < 3500:
            # Likely kcal/kg, convert to kJ/kg
            result['heating_value_kj_kg'] = result['heating_value_kj_kg'] * 4.184

    # Normalize prefecture names
    if 'prefecture' in result.columns:
        result['prefecture'] = result['prefecture'].apply(normalize)

    # Standardize facility code
    if 'facility_code' in result.columns:
        result['facility_code'] = (
            result['facility_code'].astype(str)
            .str.replace('-', '', regex=False)
            .str.replace('.0', '', regex=False)
            .str.strip()
        )

    # Standardize municipality code
    if 'muni_code' in result.columns:
        result['muni_code'] = (
            result['muni_code'].astype(str)
            .str.replace('.0', '', regex=False)
            .str.strip()
        )

    return result


def main():
    print("=" * 60)
    print("Parsing MOE Incineration Facility Data (Auto-detect)")
    print("=" * 60)

    all_years = []
    for fy in range(2005, 2025):
        print(f"  FY{fy}...", end=" ", flush=True)
        try:
            df = parse_year(fy)
            if df is not None:
                # Quick validation: check power gen column looks right
                pct_power = (df['power_capacity_kw'].notna() & (df['power_capacity_kw'] > 0)).mean() * 100 if 'power_capacity_kw' in df.columns else 0
                print(f"{len(df)} facilities, {pct_power:.1f}% with power gen")
                all_years.append(df)
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

    panel = pd.concat(all_years, ignore_index=True)

    # Compute derived variables
    panel['facility_age'] = panel['fiscal_year'] - panel['year_started']
    panel['has_power_gen'] = panel['power_capacity_kw'].notna() & (panel['power_capacity_kw'] > 0)
    panel['capacity_utilization'] = (
        panel['throughput_t_year'] / (panel['capacity_t_day'] * 365)
    ).clip(0, 1.5)

    # Energy recovery efficiency (MWh per tonne — key thesis variable)
    panel['energy_efficiency_mwh_per_t'] = (
        panel['power_generated_mwh'] / panel['throughput_t_year']
    )

    # Save
    out_path = os.path.join(PROCESSED_DIR, 'incineration_panel.csv')
    panel.to_csv(out_path, index=False, encoding='utf-8-sig')

    # --- Summary ---
    print("\n" + "=" * 60)
    print("PANEL DATASET SUMMARY")
    print("=" * 60)
    print(f"Total observations: {len(panel):,}")
    print(f"Fiscal years: {panel['fiscal_year'].min()} to {panel['fiscal_year'].max()}")
    print(f"Unique facility codes: {panel['facility_code'].nunique():,}")
    print(f"Prefectures: {panel['prefecture'].nunique()}")
    print(f"Columns: {len(panel.columns)}")

    print(f"\nFacilities per year:")
    for fy, grp in panel.groupby('fiscal_year'):
        n = len(grp)
        pct = grp['has_power_gen'].mean() * 100
        print(f"  FY{fy}: {n:,} facilities ({pct:.1f}% with power gen)")

    print(f"\nKey variable coverage (non-null %):")
    for col in ['throughput_t_year', 'capacity_t_day', 'year_started',
                'power_capacity_kw', 'power_generated_mwh', 'power_sold_mwh',
                'heating_value_kj_kg', 'facility_age', 'energy_efficiency_mwh_per_t']:
        if col in panel.columns:
            pct = panel[col].notna().mean() * 100
            print(f"  {col}: {pct:.1f}%")

    print(f"\nPower-generating facilities subsample:")
    power_sub = panel[panel['has_power_gen']]
    print(f"  Observations: {len(power_sub):,}")
    print(f"  Years: {power_sub['fiscal_year'].min()} to {power_sub['fiscal_year'].max()}")
    for col in ['power_generated_mwh', 'energy_efficiency_mwh_per_t', 'power_efficiency_pct']:
        if col in power_sub.columns:
            pct = power_sub[col].notna().mean() * 100
            print(f"  {col}: {pct:.1f}% coverage")

    print(f"\nSaved to: {os.path.abspath(out_path)}")


if __name__ == '__main__':
    main()
