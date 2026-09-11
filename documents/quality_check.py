"""
quality_check.py
Validates data/machines.csv and data/maintenance_cases.csv against the
locked schema: case_id, machine_id, component, failure, symptoms, resolution.
Checks for duplicates, missing values, and inconsistent component naming.
"""

import pandas as pd
import os

MACHINES_CSV = os.path.join("data", "machines.csv")
CASES_CSV = os.path.join("data", "maintenance_cases.csv")

REQUIRED_COLUMNS = ["case_id", "machine_id", "component", "failure", "symptoms", "resolution"]


def run():
    machines = pd.read_csv(MACHINES_CSV)
    cases = pd.read_csv(CASES_CSV)

    errors = []

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in cases.columns]
    if missing_cols:
        errors.append(f"maintenance_cases.csv missing required columns: {missing_cols}")

    for col in REQUIRED_COLUMNS:
        if col in cases.columns and cases[col].isnull().any():
            errors.append(f"Missing values found in column: {col}")

    dupes = cases[cases.duplicated("case_id", keep=False)]
    if not dupes.empty:
        errors.append(f"Duplicate case_ids: {sorted(dupes['case_id'].unique().tolist())}")

    unknown = set(cases["machine_id"]) - set(machines["machine_id"])
    if unknown:
        errors.append(f"machine_id(s) in cases not found in machines.csv: {unknown}")

    # inconsistent component naming - flag near-duplicate names (case/whitespace variants)
    normalized = cases["component"].str.strip().str.lower()
    variants = {}
    for raw, norm in zip(cases["component"], normalized):
        variants.setdefault(norm, set()).add(raw)
    inconsistent = {k: v for k, v in variants.items() if len(v) > 1}
    if inconsistent:
        errors.append(f"Inconsistent component naming variants: {inconsistent}")

    print(f"Checked {len(machines)} machines and {len(cases)} cases.")
    if errors:
        print("\nDATA QUALITY ISSUES FOUND:")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    else:
        print("All data quality checks passed.")


if __name__ == "__main__":
    run()
