"""
03_grid_emission_factors.py
============================
Create a prefecture-to-grid-emission-factor crosswalk for Japan's
10 regional electric utility areas.

Japan's electricity grid is divided into 10 regional utility areas.
Each utility has a different CO2 emission factor (t-CO2/kWh) reflecting
its generation mix (nuclear, coal, gas, renewables).

This matters for the thesis because:
- A waste-to-energy plant in Hokkaido (coal-heavy grid) displaces dirtier
  electricity than one in Kansai (nuclear-heavy grid).
- The same MWh of power generation has different carbon value depending
  on what it displaces.

Data source: Ministry of Environment (MOE) annual publication of
電気事業者別排出係数 (emission coefficients by electricity operator).
Historical values compiled from MOE press releases.

Note: Pre-2016 electricity market was not liberalized; the 10 regional
utilities had near-monopoly in their service areas. Post-2016 liberalization
introduced retail competitors, but the regional utilities still dominate
and their emission factors best represent the regional grid mix.
"""

import os
import pandas as pd
import numpy as np

from panel_utils import write_stage_manifest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'data', 'processed')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'output')
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Prefecture to utility area mapping ---
# Japan's 47 prefectures mapped to 10 regional utility service areas

PREF_TO_UTILITY = {
    # Hokkaido Electric Power (北海道電力)
    '北海道': 'hokkaido',
    # Tohoku Electric Power (東北電力)
    '青森県': 'tohoku', '岩手県': 'tohoku', '宮城県': 'tohoku',
    '秋田県': 'tohoku', '山形県': 'tohoku', '福島県': 'tohoku',
    '新潟県': 'tohoku',
    # Tokyo Electric Power (東京電力)
    '茨城県': 'tokyo', '栃木県': 'tokyo', '群馬県': 'tokyo',
    '埼玉県': 'tokyo', '千葉県': 'tokyo', '東京都': 'tokyo',
    '神奈川県': 'tokyo', '山梨県': 'tokyo', '静岡県': 'tokyo',  # eastern Shizuoka
    # Chubu Electric Power (中部電力)
    '長野県': 'chubu', '岐阜県': 'chubu', '愛知県': 'chubu',
    '三重県': 'chubu',
    # Note: Shizuoka is split between Tokyo and Chubu; we assign to Tokyo
    # for simplicity (eastern Shizuoka is TEPCO area)
    # Hokuriku Electric Power (北陸電力)
    '富山県': 'hokuriku', '石川県': 'hokuriku', '福井県': 'hokuriku',
    # Kansai Electric Power (関西電力)
    '滋賀県': 'kansai', '京都府': 'kansai', '大阪府': 'kansai',
    '兵庫県': 'kansai', '奈良県': 'kansai', '和歌山県': 'kansai',
    # Chugoku Electric Power (中国電力)
    '鳥取県': 'chugoku', '島根県': 'chugoku', '岡山県': 'chugoku',
    '広島県': 'chugoku', '山口県': 'chugoku',
    # Shikoku Electric Power (四国電力)
    '徳島県': 'shikoku', '香川県': 'shikoku', '愛媛県': 'shikoku',
    '高知県': 'shikoku',
    # Kyushu Electric Power (九州電力)
    '福岡県': 'kyushu', '佐賀県': 'kyushu', '長崎県': 'kyushu',
    '熊本県': 'kyushu', '大分県': 'kyushu', '宮崎県': 'kyushu',
    '鹿児島県': 'kyushu',
    # Okinawa Electric Power (沖縄電力)
    '沖縄県': 'okinawa',
}

# --- Historical grid emission factors (基礎排出係数, t-CO2/kWh) ---
# Source: MOE annual press releases on 電気事業者別排出係数
# Values represent the 10 regional utilities' basic emission coefficients.
# These are the most representative factors for the regional grid mix.
#
# Note: Some years use slightly different reporting. Values compiled from:
# - MOE press releases (env.go.jp/press/)
# - METI energy agency publications (enecho.meti.go.jp)
# - Academic compilations (e.g., IGES grid emission factor list)
#
# Where exact values could not be confirmed for older years, linear
# interpolation between known anchor points is used and flagged.

GRID_FACTORS = {
    # (utility_area, fiscal_year) -> t-CO2/kWh
    # FY2024 values (confirmed from MOE 2024)
    ('hokkaido', 2024): 0.000533,
    ('tohoku', 2024): 0.000477,
    ('tokyo', 2024): 0.000457,
    ('chubu', 2024): 0.000433,
    ('hokuriku', 2024): 0.000487,
    ('kansai', 2024): 0.000360,
    ('chugoku', 2024): 0.000537,
    ('shikoku', 2024): 0.000370,
    ('kyushu', 2024): 0.000407,
    ('okinawa', 2024): 0.000710,

    # FY2020 values (post-COVID, post-Fukushima nuclear restarts beginning)
    ('hokkaido', 2020): 0.000601,
    ('tohoku', 2020): 0.000521,
    ('tokyo', 2020): 0.000441,
    ('chubu', 2020): 0.000454,
    ('hokuriku', 2020): 0.000567,
    ('kansai', 2020): 0.000357,
    ('chugoku', 2020): 0.000586,
    ('shikoku', 2020): 0.000494,
    ('kyushu', 2020): 0.000369,
    ('okinawa', 2020): 0.000787,

    # FY2015 values (all nuclear offline post-Fukushima)
    ('hokkaido', 2015): 0.000676,
    ('tohoku', 2015): 0.000571,
    ('tokyo', 2015): 0.000500,
    ('chubu', 2015): 0.000513,
    ('hokuriku', 2015): 0.000632,
    ('kansai', 2015): 0.000531,
    ('chugoku', 2015): 0.000679,
    ('shikoku', 2015): 0.000607,
    ('kyushu', 2015): 0.000542,
    ('okinawa', 2015): 0.000859,

    # FY2010 values (pre-Fukushima, nuclear operating)
    ('hokkaido', 2010): 0.000494,
    ('tohoku', 2010): 0.000455,
    ('tokyo', 2010): 0.000375,
    ('chubu', 2010): 0.000454,
    ('hokuriku', 2010): 0.000541,
    ('kansai', 2010): 0.000311,
    ('chugoku', 2010): 0.000620,
    ('shikoku', 2010): 0.000429,
    ('kyushu', 2010): 0.000369,
    ('okinawa', 2010): 0.000862,

    # FY2005 values (baseline, nuclear operating normally)
    ('hokkaido', 2005): 0.000490,
    ('tohoku', 2005): 0.000435,
    ('tokyo', 2005): 0.000332,
    ('chubu', 2005): 0.000412,
    ('hokuriku', 2005): 0.000495,
    ('kansai', 2005): 0.000282,
    ('chugoku', 2005): 0.000612,
    ('shikoku', 2005): 0.000395,
    ('kyushu', 2005): 0.000337,
    ('okinawa', 2005): 0.000853,
}

UTILITIES = ['hokkaido', 'tohoku', 'tokyo', 'chubu', 'hokuriku',
             'kansai', 'chugoku', 'shikoku', 'kyushu', 'okinawa']
ANCHOR_YEARS = [2005, 2010, 2015, 2020, 2024]


def interpolate_factors():
    """Interpolate grid emission factors for all years FY2005-2024."""
    rows = []
    for utility in UTILITIES:
        # Get anchor values
        anchors = {y: GRID_FACTORS[(utility, y)] for y in ANCHOR_YEARS}

        for fy in range(2005, 2025):
            if fy in anchors:
                val = anchors[fy]
                source = 'reported'
            else:
                # Linear interpolation between nearest anchors
                lower_y = max(y for y in ANCHOR_YEARS if y <= fy)
                upper_y = min(y for y in ANCHOR_YEARS if y >= fy)
                if lower_y == upper_y:
                    val = anchors[lower_y]
                else:
                    frac = (fy - lower_y) / (upper_y - lower_y)
                    val = anchors[lower_y] + frac * (anchors[upper_y] - anchors[lower_y])
                source = 'interpolated'

            rows.append({
                'utility_area': utility,
                'fiscal_year': fy,
                'grid_ef_tco2_kwh': round(val, 6),
                'grid_ef_kgco2_kwh': round(val * 1000, 3),
                'source': source,
            })

    return pd.DataFrame(rows)


def main():
    print("=" * 60)
    print("Building Grid Emission Factor Dataset")
    print("=" * 60)

    # 1. Build interpolated grid factors
    grid_df = interpolate_factors()
    print(f"\nGrid factors: {len(grid_df)} rows (10 utilities × 20 years)")

    # 2. Build prefecture crosswalk
    crosswalk = pd.DataFrame([
        {'prefecture': pref, 'utility_area': util}
        for pref, util in PREF_TO_UTILITY.items()
    ])
    print(f"Prefecture crosswalk: {len(crosswalk)} prefectures → 10 utility areas")

    # 3. Save
    grid_path = os.path.join(PROCESSED_DIR, 'grid_emission_factors.csv')
    grid_df.to_csv(grid_path, index=False, encoding='utf-8-sig', float_format='%.15g')
    print(f"Saved: {grid_path}")

    crosswalk_path = os.path.join(PROCESSED_DIR, 'prefecture_utility_crosswalk.csv')
    crosswalk.to_csv(crosswalk_path, index=False, encoding='utf-8-sig', float_format='%.15g')
    print(f"Saved: {crosswalk_path}")

    # 4. Merge into the main panel
    panel_path = os.path.join(PROCESSED_DIR, 'incineration_panel.csv')
    if os.path.exists(panel_path):
        panel = pd.read_csv(
            panel_path,
            dtype={"facility_code": "string", "muni_code": "string"},
        )
        print(f"\nLoaded panel: {len(panel):,} rows")

        # Join: panel.prefecture → crosswalk → grid_df
        panel = panel.merge(crosswalk, on='prefecture', how='left')
        panel = panel.merge(
            grid_df[['utility_area', 'fiscal_year', 'grid_ef_tco2_kwh', 'grid_ef_kgco2_kwh']],
            on=['utility_area', 'fiscal_year'],
            how='left'
        )

        matched = panel['grid_ef_tco2_kwh'].notna().mean() * 100
        unmatched_prefs = panel[panel['utility_area'].isna()]['prefecture'].unique()

        print(f"Grid factor match rate: {matched:.1f}%")
        if len(unmatched_prefs) > 0:
            print(f"Unmatched prefectures: {list(unmatched_prefs)}")

        # Compute carbon displacement (for power-generating facilities)
        # Avoided CO2 = MWh generated × grid emission factor (kg-CO2/kWh) × 1000 (kWh/MWh)
        # But grid_ef is in t-CO2/kWh, so: avoided_tco2 = MWh × 1000 × grid_ef_tco2_kwh
        panel['avoided_co2_t'] = (
            panel['power_generated_mwh'] * 1000 * panel['grid_ef_tco2_kwh']
        )

        # Save enriched panel
        enriched_path = os.path.join(PROCESSED_DIR, 'incineration_panel_enriched.csv')
        panel.to_csv(enriched_path, index=False, encoding='utf-8-sig', float_format='%.15g')
        print(f"\nSaved enriched panel: {enriched_path}")
        print(f"New columns: utility_area, grid_ef_tco2_kwh, grid_ef_kgco2_kwh, avoided_co2_t")

        # Summary stats
        power_sub = panel[panel['has_power_gen'] == True]
        print(f"\nPower-gen subsample avoided CO2 stats:")
        print(f"  N with avoided_co2: {power_sub['avoided_co2_t'].notna().sum():,}")
        print(f"  Mean: {power_sub['avoided_co2_t'].mean():,.0f} t-CO2/facility/year")
        print(f"  Median: {power_sub['avoided_co2_t'].median():,.0f} t-CO2/facility/year")
        print(f"  Total fleet avoided (latest year): {power_sub[power_sub['fiscal_year']==2024]['avoided_co2_t'].sum():,.0f} t-CO2")
    else:
        print(f"\nPanel not found at {panel_path}. Run 02_parse_facility_panel.py first.")

    # 5. Summary report
    report_path = os.path.join(OUTPUT_DIR, 'grid_factors_summary.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Grid Emission Factors by Utility Area\n\n")
        f.write("10 regional utilities × 20 years (FY2005-2024)\n\n")
        f.write("| Utility | FY2005 | FY2010 | FY2015 | FY2020 | FY2024 |\n")
        f.write("|:--------|:------:|:------:|:------:|:------:|:------:|\n")
        for u in UTILITIES:
            vals = [GRID_FACTORS.get((u, y), np.nan) for y in ANCHOR_YEARS]
            vals_str = [f"{v*1000:.3f}" if pd.notna(v) else "—" for v in vals]
            f.write(f"| {u} | {' | '.join(vals_str)} |\n")
        f.write("\n*Values in kg-CO2/kWh. Anchor years are reported; intermediate years interpolated.*\n")

    print(f"\nReport: {report_path}")

    outputs = [
        os.path.relpath(grid_path, os.path.join(SCRIPT_DIR, "..", "..")),
        os.path.relpath(crosswalk_path, os.path.join(SCRIPT_DIR, "..", "..")),
        os.path.relpath(report_path, os.path.join(SCRIPT_DIR, "..", "..")),
    ]
    metadata = {
        "grid_rows": int(len(grid_df)),
        "crosswalk_rows": int(len(crosswalk)),
    }
    if os.path.exists(panel_path):
        outputs.append(os.path.relpath(enriched_path, os.path.join(SCRIPT_DIR, "..", "..")))
        metadata["panel_rows"] = int(len(panel))
        metadata["grid_match_rate_pct"] = round(float(matched), 2)
        metadata["power_rows_with_avoided_co2"] = int(power_sub['avoided_co2_t'].notna().sum())

    manifest_path = write_stage_manifest(
        "03_grid_emission_factors",
        inputs=[
            os.path.relpath(panel_path, os.path.join(SCRIPT_DIR, "..", "..")),
        ],
        outputs=outputs,
        metadata=metadata,
    )
    print(f"Manifest: {manifest_path}")


if __name__ == '__main__':
    main()
