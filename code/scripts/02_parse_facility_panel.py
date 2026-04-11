"""
02_parse_facility_panel.py
==========================
Parse all 20 years of MOE incineration facility Excel files into a single
panel dataset with standardized column names.

The header structure differs across eras:
- FY2005: headers at row 0, data at row 1+ (some at row 2), 44 cols
- FY2006-2009: headers at rows 0-5, data at row 6, ~80 cols (facility code format varies)
- FY2010+: headers at rows 0-5, data at row 6, 78-100 cols

Core variables extracted (available in all years):
- prefecture: Prefecture name
- muni_code: Municipality code
- facility_code: Facility code (standardized)
- facility_name: Facility name
- throughput_t_year: Annual waste processed (t/year)
- capacity_t_day: Total facility capacity (t/day)
- n_furnaces: Number of furnaces
- year_started: Fiscal year operations began
- heat_util_status: Waste heat utilization description
- heat_util_mj: Total heat utilization (MJ) — actual if available, else spec
- power_capacity_kw: Power generation capacity (kW)
- power_efficiency_pct: Power generation efficiency (%)
- power_generated_mwh: Total electricity generated (MWh)
- power_sold_mwh: Electricity sold externally (MWh) — from FY2016+
- heating_value_kj_kg: Lower heating value of waste (kJ/kg)
- furnace_type: Type of furnace
- operation_mode: Continuous/batch operation
- fiscal_year: The fiscal year of this observation
"""

import os
import sys
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'raw', 'facility_annual')
PROCESSED_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'processed')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Column mappings by era ---
# Each mapping: {standardized_name: column_index}

MAP_2005 = {
    'prefecture': 1,
    'muni_code': 2,
    'facility_code': 3,
    'facility_name': 7,
    'throughput_t_year': 8,
    'resource_recovery_t_year': 9,
    'waste_type': 12,
    'facility_type': 13,
    'furnace_type': 14,
    'operation_mode': 15,
    'capacity_t_day': 16,
    'n_furnaces': 17,
    'year_started': 18,
    'heat_util_status': 19,
    'heat_util_mj': 20,
    'power_capacity_kw': 21,
    'power_efficiency_pct': 22,
    'power_generated_mwh': 23,
    'heating_value_kj_kg': 41,  # kcal/kg in 2005, needs conversion
}

# FY2006-2009 have a slightly different layout with an extra column for facility setter
MAP_2006_2009 = {
    'prefecture': 0,
    'muni_code': 1,
    'facility_code': 2,
    'facility_name': 5,
    'throughput_t_year': 6,
    'resource_recovery_t_year': 7,
    'waste_type': 10,
    'facility_type': 12,
    'furnace_type': 14,
    'operation_mode': 15,
    'capacity_t_day': 16,
    'n_furnaces': 17,
    'year_started': 18,
    'heat_util_status': 19,
    'heat_util_mj_spec': 20,
    'heat_util_mj_actual': 22,
    'power_capacity_kw': 24,
    'power_efficiency_pct': 25,
    'power_generated_mwh': 26,
    'power_external_mwh': 27,
    'heating_value_kj_kg': 46,
}

# FY2010-2015 (similar to 2006-2009 but may have minor shifts)
MAP_2010_2015 = MAP_2006_2009.copy()

# FY2016+ dropped the facility setter column, shifted some columns
MAP_2016_PLUS = {
    'prefecture': 0,
    'muni_code': 1,
    'facility_code': 2,
    'facility_name': 4,
    'throughput_t_year': 5,
    'resource_recovery_t_year': 6,
    'waste_type': 9,
    'facility_type': 11,
    'furnace_type': 13,
    'operation_mode': 14,
    'processing_scheme': 15,
    'capacity_t_day': 16,
    'n_furnaces': 17,
    'year_started': 18,
    'heat_util_status': 19,
    'heat_util_mj_spec': 20,
    'heat_util_mj_actual': 22,
    'power_capacity_kw': 24,
    'power_efficiency_pct': 25,
    'power_generated_mwh': 26,
    'power_external_mwh': 27,
    'power_sold_mwh': 28,
    'sell_revenue_yen': 29,
    'heating_value_kj_kg': 66,
}

# FY2024 added facility address at col 5, shifting everything after
MAP_2024 = {
    'prefecture': 0,
    'muni_code': 1,
    'facility_code': 2,
    'facility_name': 4,
    'facility_address': 5,
    'throughput_t_year': 6,
    'resource_recovery_t_year': 7,
    'waste_type': 10,
    'facility_type': 12,
    'furnace_type': 14,
    'operation_mode': 15,
    'processing_scheme': 16,
    'capacity_t_day': 17,
    'n_furnaces': 18,
    'year_started': 19,
    'heat_util_status': 20,
    'heat_util_mj_spec': 21,
    'heat_util_mj_actual': 23,
    'power_capacity_kw': 25,
    'power_efficiency_pct': 26,
    'power_generated_mwh': 27,
    'power_external_mwh': 28,
    'power_sold_mwh': 29,
    'sell_revenue_yen': 30,
    'heating_value_kj_kg': 67,
}


def get_mapping(fy):
    """Return column mapping and parsing config for a fiscal year."""
    if fy == 2005:
        return MAP_2005, {'header_rows': 1, 'data_start': 1, 'engine': 'xlrd'}
    elif 2006 <= fy <= 2009:
        return MAP_2006_2009, {'header_rows': 6, 'data_start': 6, 'engine': 'xlrd'}
    elif 2010 <= fy <= 2015:
        return MAP_2010_2015, {'header_rows': 6, 'data_start': 6,
                               'engine': 'xlrd' if fy != 2014 else 'openpyxl'}
    elif 2016 <= fy <= 2023:
        return MAP_2016_PLUS, {'header_rows': 6, 'data_start': 6, 'engine': 'openpyxl'}
    elif fy >= 2024:
        return MAP_2024, {'header_rows': 6, 'data_start': 6, 'engine': 'openpyxl'}
    else:
        raise ValueError(f"No mapping for FY{fy}")


def parse_year(fy):
    """Parse a single fiscal year's facility file into a standardized DataFrame."""
    # Find the file
    for ext in ['xlsx', 'xls']:
        fpath = os.path.join(RAW_DIR, f'fy{fy}_incineration.{ext}')
        if os.path.exists(fpath):
            break
    else:
        print(f"  FY{fy}: file not found, skipping")
        return None

    mapping, config = get_mapping(fy)

    # Read raw data
    df_raw = pd.read_excel(
        fpath, sheet_name=0, header=None,
        engine=config['engine']
    )

    # Skip header rows
    df_data = df_raw.iloc[config['data_start']:].copy()
    df_data = df_data.reset_index(drop=True)

    # Drop rows where prefecture is NaN (footer/summary rows)
    pref_col = mapping['prefecture']
    df_data = df_data[df_data.iloc[:, pref_col].notna()].copy()
    df_data = df_data.reset_index(drop=True)

    # Extract columns
    result = pd.DataFrame()

    for col_name, col_idx in mapping.items():
        if col_idx < df_data.shape[1]:
            result[col_name] = df_data.iloc[:, col_idx].values
        else:
            result[col_name] = np.nan

    # Set fiscal year as a proper column
    result['fiscal_year'] = fy

    # Standardize: merge spec/actual heat utilization
    if 'heat_util_mj_actual' in result.columns and 'heat_util_mj_spec' in result.columns:
        result['heat_util_mj'] = result['heat_util_mj_actual'].fillna(
            result['heat_util_mj_spec']
        )
    elif 'heat_util_mj' not in result.columns:
        result['heat_util_mj'] = np.nan

    # FY2005 heating value is in kcal/kg, convert to kJ/kg (1 kcal = 4.184 kJ)
    if fy == 2005 and 'heating_value_kj_kg' in result.columns:
        result['heating_value_kj_kg'] = pd.to_numeric(
            result['heating_value_kj_kg'], errors='coerce'
        ) * 4.184

    # Convert numeric columns
    numeric_cols = [
        'throughput_t_year', 'resource_recovery_t_year', 'capacity_t_day',
        'n_furnaces', 'year_started', 'heat_util_mj', 'power_capacity_kw',
        'power_efficiency_pct', 'power_generated_mwh', 'power_external_mwh',
        'power_sold_mwh', 'sell_revenue_yen', 'heating_value_kj_kg',
    ]
    for col in numeric_cols:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce')

    # Standardize facility code (remove dashes for consistency)
    if 'facility_code' in result.columns:
        result['facility_code'] = (
            result['facility_code']
            .astype(str)
            .str.replace('-', '', regex=False)
            .str.strip()
        )

    # Standardize municipality code
    if 'muni_code' in result.columns:
        result['muni_code'] = (
            result['muni_code']
            .astype(str)
            .str.replace('.0', '', regex=False)
            .str.strip()
        )

    return result


def main():
    print("=" * 60)
    print("Parsing MOE Incineration Facility Data")
    print("=" * 60)

    all_years = []
    for fy in range(2005, 2025):
        print(f"  FY{fy}...", end=" ", flush=True)
        try:
            df = parse_year(fy)
            if df is not None:
                print(f"{len(df)} facilities, {len(df.columns)} cols")
                all_years.append(df)
            else:
                print("SKIPPED")
        except Exception as e:
            print(f"ERROR: {e}")

    # Combine all years
    panel = pd.concat(all_years, ignore_index=True)

    # Keep only the standardized core columns
    core_cols = [
        'fiscal_year', 'prefecture', 'muni_code', 'facility_code',
        'facility_name', 'throughput_t_year', 'capacity_t_day',
        'n_furnaces', 'year_started', 'waste_type', 'facility_type',
        'furnace_type', 'operation_mode', 'heat_util_status',
        'heat_util_mj', 'power_capacity_kw', 'power_efficiency_pct',
        'power_generated_mwh', 'power_sold_mwh', 'sell_revenue_yen',
        'heating_value_kj_kg',
    ]
    # Only keep columns that exist
    core_cols = [c for c in core_cols if c in panel.columns]
    panel = panel[core_cols]

    # Compute derived variables
    panel['facility_age'] = panel['fiscal_year'] - pd.to_numeric(
        panel['year_started'], errors='coerce'
    )
    panel['has_power_gen'] = panel['power_capacity_kw'].notna() & (
        panel['power_capacity_kw'] > 0
    )
    panel['capacity_utilization'] = (
        panel['throughput_t_year'] / (panel['capacity_t_day'] * 365)
    ).clip(0, 1.5)  # cap at 150% to handle edge cases

    # Save
    out_path = os.path.join(PROCESSED_DIR, 'incineration_panel.csv')
    panel.to_csv(out_path, index=False, encoding='utf-8-sig')

    # --- Summary report ---
    print("\n" + "=" * 60)
    print("PANEL DATASET SUMMARY")
    print("=" * 60)
    print(f"Total observations: {len(panel):,}")
    print(f"Fiscal years: {panel['fiscal_year'].min()} to {panel['fiscal_year'].max()}")
    print(f"Unique facility codes: {panel['facility_code'].nunique():,}")
    print(f"Prefectures: {panel['prefecture'].nunique()}")
    print(f"Columns: {len(panel.columns)}")
    print(f"\nFacilities per year:")
    for fy, count in panel.groupby('fiscal_year').size().items():
        pct_power = panel[panel['fiscal_year'] == fy]['has_power_gen'].mean() * 100
        print(f"  FY{fy}: {count:,} facilities ({pct_power:.1f}% with power generation)")

    print(f"\nKey variable coverage (non-null %):")
    for col in ['throughput_t_year', 'capacity_t_day', 'year_started',
                'power_capacity_kw', 'power_generated_mwh', 'heating_value_kj_kg',
                'facility_age', 'has_power_gen', 'capacity_utilization']:
        if col in panel.columns:
            pct = panel[col].notna().mean() * 100
            print(f"  {col}: {pct:.1f}%")

    print(f"\nSaved to: {os.path.abspath(out_path)}")

    # Also save a summary report
    report_path = os.path.join(OUTPUT_DIR, 'panel_summary.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Incineration Facility Panel Dataset Summary\n\n")
        f.write(f"- **Observations:** {len(panel):,}\n")
        f.write(f"- **Years:** FY{panel['fiscal_year'].min()} to FY{panel['fiscal_year'].max()}\n")
        f.write(f"- **Unique facilities:** {panel['facility_code'].nunique():,}\n")
        f.write(f"- **Prefectures:** {panel['prefecture'].nunique()}\n")
        f.write(f"- **Columns:** {len(panel.columns)}\n\n")

        f.write("## Facilities per year\n\n")
        f.write("| FY | Facilities | % with power gen |\n")
        f.write("|:---|:----------:|:----------------:|\n")
        for fy, count in panel.groupby('fiscal_year').size().items():
            pct = panel[panel['fiscal_year'] == fy]['has_power_gen'].mean() * 100
            f.write(f"| {fy} | {count:,} | {pct:.1f}% |\n")

    print(f"Report saved to: {os.path.abspath(report_path)}")


if __name__ == '__main__':
    main()
