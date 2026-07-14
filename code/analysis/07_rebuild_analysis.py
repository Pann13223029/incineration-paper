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
    "02b_build_raw_data_manifest.py",
    "02_parse_facility_panel.py",
    "02a_build_facility_identity.py",
    "02c_build_linkage_validation_packet.py",
    "04_eda_facility.py",
    "05_fleet_decomposition.py",
    "05a_power_adoption.py",
    "05_panel_regression.py",
    "05b_scientific_revision.py",
    "06_robustness.py",
    "06a_data_quality_sensitivity.py",
    "06b_identifier_gap_audit.py",
    "08_verify_claims.py",
]


def main():
    print("=" * 60)
    print("Rebuilding analysis artifacts and verifying paper-facing claims")
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
