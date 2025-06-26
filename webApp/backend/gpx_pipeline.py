# backend/gpx_pipeline.py

import os
import joblib
import pandas as pd
import gpxpy

MODEL_PATH  = os.path.join("model", "model.pkl")
SCALER_PATH = os.path.join("model", "scaler.pkl")
DIFF_SCALER_PATH = os.path.join("model", "difficulty_scaler.pkl")
DIFF_KMEANS_PATH = os.path.join("model", "difficulty_kmeans.pkl")
DIFF_MAP_PATH    = os.path.join("model", "difficulty_cluster_map.pkl")
DIFF_NN_PATH      = os.path.join("model", "difficulty_nn.pkl")
DIFF_DF_RAW_PATH  = os.path.join("model", "difficulty_df_raw.pkl")
NAMES_DF_PATH = os.path.join("model", "df_raw_copy.pkl")


# Load once
_model  = joblib.load(MODEL_PATH)
_scaler = joblib.load(SCALER_PATH)
_diff_scaler      = joblib.load(DIFF_SCALER_PATH)
_diff_kmeans      = joblib.load(DIFF_KMEANS_PATH)
_diff_cluster_map = joblib.load(DIFF_MAP_PATH)
_diff_nn       = joblib.load(DIFF_NN_PATH)
_diff_df_raw   = joblib.load(DIFF_DF_RAW_PATH)
_names_df     = joblib.load(NAMES_DF_PATH)


# print(_names_df.columns)   # should include 'name'
# print(_names_df.head())

DIFF_FEATURES = [
    "length_3d",
    "min_elevation",
    "max_elevation",
    "uphill",
    "downhill",
    "break_time",
    "duration"
]

def secs_to_hm(seconds):
    """Convert seconds to 'Xh Ym' format."""
    seconds = float(seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m"

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
    hours = int(pred_seconds // 3600)
    minutes = int((pred_seconds % 3600) // 60)
    # Debug print showing hours and minutes
    # print(f"Predicted duration:({hours}h {minutes}m)")

 
    # 6. Return raw stats + prediction
    stats = {
        "length_3d_m":           round(length_3d, 2),
        "uphill_m":              round(uphill, 2),
        "downhill_m":            round(downhill, 2),
        "min_elevation_m":       round(min_elev, 2),
        "max_elevation_m":       round(max_elev, 2),
        "break_time_sec":        round((pts[-1].time - pts[0].time).total_seconds() - duration_obs, 2),
        "observed_duration_sec": round(duration_obs, 2),
        "predicted_duration_hm": f"{hours}h {minutes}m",
    }

    # Recompute break_time
    t0, t1     = pts[0].time, pts[-1].time
    total_time = (t1 - t0).total_seconds()
    break_time = max(0.0, total_time - duration_obs)

    diff_df = pd.DataFrame([{
        "length_3d":     length_3d,
        "min_elevation": min_elev,
        "max_elevation": max_elev,
        "uphill":        uphill,
        "downhill":      downhill,
        "break_time":    break_time,
        "duration":      duration_obs,
    }])

    # Scale + predict cluster
    Xd          = _diff_scaler.transform(diff_df)
    cluster_id  = int(_diff_kmeans.predict(Xd)[0])
    diff_label  = _diff_cluster_map[cluster_id]
    # print(f"Predicted difficulty: {diff_label}")    

    # Append to stats
    stats["predicted_difficulty"] = diff_label

    # 5. Nearest-hikes recommendation
    distances, indices = _diff_nn.kneighbors(Xd, n_neighbors=3)
    neigh_df = _diff_df_raw.iloc[indices[0]].reset_index(drop=True)
    neighbor_ids = indices[0]
    #neigh_df["name"] = _names_df["name"].iloc[neighbor_ids].values
    # Convert units:
    # - duration to hours/minutes
    # - other stats remain in meters
    neigh_df["duration_hm"]      = neigh_df["duration"].apply(secs_to_hm)
    neigh_df["length_3d_m"]      = neigh_df["length_3d"]
    neigh_df["uphill_m"]         = neigh_df["uphill"]
    neigh_df["downhill_m"]       = neigh_df["downhill"]
    neigh_df["min_elevation_m"]  = neigh_df["min_elevation"]
    neigh_df["max_elevation_m"]  = neigh_df["max_elevation"]
    neigh_df["break_time_hm"]    = neigh_df["break_time"].apply(secs_to_hm)

    # Only keep the converted fields + optionally distance ranking
    stats = {
        "length_3d_m":           round(length_3d, 2),
        "uphill_m":              round(uphill, 2),
        "downhill_m":            round(downhill, 2),
        "min_elevation_m":       round(min_elev, 2),
        "max_elevation_m":       round(max_elev, 2),
        "break_time_sec":        round(break_time, 2),
        "observed_duration_hm":  secs_to_hm(duration_obs),
        "predicted_duration_hm": f"{hours}h {minutes}m",
        "predicted_difficulty":  diff_label,
        "nearest_hikes":         neigh_df[[
            "duration_hm",
            "length_3d_m",
            "uphill_m",
            "downhill_m",
            "break_time_hm"
        ]].to_dict(orient="records")
    }

    return stats