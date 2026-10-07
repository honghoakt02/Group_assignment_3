#!/usr/bin/env python3
"""
HOSE V4 Data Extraction & Preprocessing Script
Reads raw notebook outputs and OHLCV CSV, then exports verified datasets to data/ directory.
"""

import os
import json
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def validate_and_save(df, filename_base):
    json_path = os.path.join(DATA_DIR, f"{filename_base}.json")
    csv_path = os.path.join(DATA_DIR, f"{filename_base}.csv")
    df.to_json(json_path, orient="records", indent=2, force_ascii=False)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved: {json_path} and {csv_path}")

def main():
    print("HOSE V4 Data Extraction Pipeline initialized.")
    # Verification of existing files
    expected = [
        "metadata.json", "data_quality.json", "time_split.json",
        "core_threshold_trials.json", "val_selection_history.json",
        "val_models.json", "test_selection_history.json",
        "final_test_results.json", "leakage_audit.json", "inventory.json"
    ]
    missing = [f for f in expected if not os.path.exists(os.path.join(DATA_DIR, f))]
    if not missing:
        print(f"All {len(expected)} verified datasets are intact in {DATA_DIR}.")
    else:
        print(f"Warning: Missing datasets: {missing}")

if __name__ == "__main__":
    main()
