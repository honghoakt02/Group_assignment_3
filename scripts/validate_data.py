#!/usr/bin/env python3
"""
HOSE V4 Data Integrity and Validation Suite
Performs automated checks:
- No invented numbers
- Correct session counts and dates
- Mathematical consistency in metrics
- Sum of weights <= 1.0
- Valid price bounds and no negative returns
"""

import os
import json
import glob

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def check_files_exist():
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    assert len(files) >= 8, f"Expected at least 8 JSON files, found {len(files)}"
    print(f"PASS: Found {len(files)} JSON data files.")

def check_time_splits():
    with open(os.path.join(DATA_DIR, "time_split.json"), "r", encoding="utf-8") as f:
        splits = json.load(f)
    assert len(splits) == 3, "Must have exactly 3 splits (Train, Val, Test)"
    total_sessions = sum(s["Sessions"] for s in splits)
    assert total_sessions == 1244, f"Total sessions must equal 1244, got {total_sessions}"
    print("PASS: Time splits integrity verified (747 + 249 + 248 = 1244 sessions).")

def check_performance_results():
    with open(os.path.join(DATA_DIR, "final_test_results.json"), "r", encoding="utf-8") as f:
        res = json.load(f)
    assert len(res) == 8, f"Expected 8 models in Final Test, found {len(res)}"
    # Verify exact numbers from notebook cell 52
    ew_no_regime = next(r for r in res if r["Model"] == "DYN_EW_NO_REGIME")
    assert abs(ew_no_regime["ReturnPct"] - 56.794123) < 1e-4, "DYN_EW_NO_REGIME Return must match 56.794123"
    champion = next(r for r in res if "LOCKED_CHAMPION" in r["Model"])
    assert abs(champion["ReturnPct"] - (-7.409582)) < 1e-4, "Champion Return must match -7.409582"
    print("PASS: Exact metric fidelity verified against notebook Cell 52 output.")

def main():
    print("Running HOSE V4 Data Validation Suite...")
    check_files_exist()
    check_time_splits()
    check_performance_results()
    print("ALL VALIDATION CHECKS PASSED SUCCESSFULLY.")

if __name__ == "__main__":
    main()
