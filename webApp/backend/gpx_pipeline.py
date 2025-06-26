# backend/gpx_pipeline.py

import os
import joblib
import pandas as pd
import gpxpy

MODEL_PATH  = os.path.join("model", "model.pkl")
SCALER_PATH = os.path.join("model", "scaler.pkl")

# Load once
_model  = joblib.load(MODEL_PATH)
_scaler = joblib.load(SCALER_PATH)

def analyze_gpx_stream(stream):
    # 1. Parse
    gpx = gpxpy.parse(stream)

    # 2. Flatten points
    pts = [
        pt
        for tr in gpx.tracks
        for seg in tr.segments
        for pt in seg.points
    ]
    if len(pts) < 2:
        raise ValueError("Not enough data points")

    # 3. Compute core stats (the exact features your scaler/model expect)
    length_3d    = gpx.length_3d()               # meters
    duration_obs = gpx.get_duration() or 0       # seconds
    uphill, downhill = gpx.get_uphill_downhill() # meters up/down
    elevations   = [pt.elevation for pt in pts]
    min_elev, max_elev = float(min(elevations)), float(max(elevations))

    # 4. Build DataFrame with exactly those five columns
    feat_df = pd.DataFrame([{
        "length_3d":     length_3d,
        "min_elevation": min_elev,
        "max_elevation": max_elev,
        "uphill":        uphill,
        "downhill":      downhill,
    }])

    # 5. Scale & predict
    X_scaled     = _scaler.transform(feat_df)
    pred_seconds = float(_model.predict(X_scaled)[0])
    pred_hours   = pred_seconds / 3600.0
    print(f"Predicted duration: {pred_seconds} seconds ({pred_hours} hours)")

    # 6. Return raw stats + prediction
    return {
        "length_3d_m":           round(length_3d, 2),
        "uphill_m":              round(uphill, 2),
        "downhill_m":            round(downhill, 2),
        "min_elevation_m":       round(min_elev, 2),
        "max_elevation_m":       round(max_elev, 2),
        "observed_duration_sec": round(duration_obs, 2),
        "predicted_duration_hr": round(pred_hours, 2),
    }
