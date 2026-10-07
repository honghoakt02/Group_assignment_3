"""
HOSE V4 Quantitative Finance Backend API (FastAPI)
Serves authentic experimental data from data/ directory to the frontend dashboard.
"""

import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="HOSE V4 Quantitative Dashboard API",
    description="RESTful API providing verified datasets from HOSE V4 Nested Walk-Forward Research",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def read_json_data(filename: str):
    path = DATA_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found in data layer")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "HOSE V4 API", "data_layer": str(DATA_DIR)}

@app.get("/api/metadata")
def get_metadata():
    return read_json_data("metadata.json")

@app.get("/api/inventory")
def get_inventory():
    return read_json_data("inventory.json")

@app.get("/api/data/time-split")
def get_time_split():
    return read_json_data("time_split.json")

@app.get("/api/data/threshold-trials")
def get_threshold_trials():
    return read_json_data("core_threshold_trials.json")

@app.get("/api/data/val-selection")
def get_val_selection():
    return read_json_data("val_selection_history.json")

@app.get("/api/data/val-models")
def get_val_models():
    return read_json_data("val_models.json")

@app.get("/api/data/test-selection")
def get_test_selection():
    return read_json_data("test_selection_history.json")

@app.get("/api/data/final-test")
def get_final_test():
    return read_json_data("final_test_results.json")

@app.get("/api/data/leakage-audit")
def get_leakage_audit():
    return read_json_data("leakage_audit.json")

@app.get("/api/data/data-quality")
def get_data_quality():
    return read_json_data("data_quality.json")

@app.get("/api/data/sample-ranking")
def get_sample_ranking():
    return read_json_data("sample_ranking.json")

@app.get("/api/data/sample-features")
def get_sample_features():
    return read_json_data("stock_features_sample.json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
