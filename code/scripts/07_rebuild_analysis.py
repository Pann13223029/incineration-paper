"""
07_rebuild_analysis.py
======================
Rebuild the published analysis artifacts from the checked-in raw data.
"""

from __future__ import annotations

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

STAGES = [
    "02_parse_facility_panel.py",
    "03_grid_emission_factors.py",
    "04_eda_facility.py",
    "05_panel_regression.py",
    "06_robustness.py",
]


def main():
    print("=" * 60)
    print("Rebuilding analysis artifacts from raw data")
    print("=" * 60)

    for script_name in STAGES:
        path = os.path.join(SCRIPT_DIR, script_name)
        print(f"\n>>> Running {script_name}")
        subprocess.run([sys.executable, path], check=True)

    print("\n" + "=" * 60)
    print("REBUILD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
