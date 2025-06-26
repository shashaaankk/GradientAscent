# src/Preprocessor.py

import os
import zipfile
import requests
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report

# ─── 1) Download & extract ─────────────────────────────────────────────────────
data_dir    = "data"
zip_path    = os.path.join(data_dir, "gpx-hike-tracks.zip")
download_url = "https://www.kaggle.com/api/v1/datasets/download/roccoli/gpx-hike-tracks"

os.makedirs(data_dir, exist_ok=True)
if not os.path.exists(zip_path):
    print("Downloading dataset...")
    r = requests.get(download_url, allow_redirects=True)
    r.raise_for_status()
    with open(zip_path, "wb") as f:
        f.write(r.content)
    print("Download complete.")

print("Extracting files...")
with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(data_dir)
print("Extraction complete.")

csv_path = os.path.join(data_dir, "gpx-tracks-from-hikr.org.csv")

# ─── 2) Load & clean ────────────────────────────────────────────────────────────
df = pd.read_csv(csv_path)

# Basic dropna on essential timestamp columns
df = df.dropna(subset=["start_time", "end_time"])

# Remove zero-length or zero-duration tracks
df = df[df["start_time"] != df["end_time"]]
df = df[df["length_3d"]  != 0]
df = df[df["moving_time"] != 0]

# Parse times
df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
df["end_time"]   = pd.to_datetime(df["end_time"],   errors="coerce")

# Compute derived columns
df["duration"]   = df["moving_time"]  # seconds moving
df["break_time"] = (df["end_time"] - df["start_time"]).dt.total_seconds() - df["moving_time"]
df["speed"]      = df["length_3d"] / df["duration"]

# Filter outliers
df = df[df["break_time"] >= 0]
df = df[df["break_time"] < 1.5 * df["duration"]]
df = df[df["speed"] < 5]

# ─── 3) Select features + keep 'name' metadata ─────────────────────────────────
# Ensure your CSV has a 'name' column; if not, derive it here.
# e.g. df["name"] = df["filename"].str.replace(".gpx","").str.replace("_"," ").str.title()
selected = df[[
    "name",           # preserve for later lookup
    "duration",
    "length_3d",
    "min_elevation",
    "max_elevation",
    "uphill",
    "downhill",
    "break_time"
]]

# ─── 4) Drop rows with any missing numeric data ────────────────────────────────
selected = selected.dropna(subset=[
    "duration",
    "length_3d",
    "min_elevation",
    "max_elevation",
    "uphill",
    "downhill",
    "break_time"
])

# ─── 5) Prepare X, y for training (drop 'name') ────────────────────────────────
X = selected.drop(columns=["name"])
y = df.loc[selected.index, "difficulty"].str[1].astype(int)

# ─── 6) Scale & split ──────────────────────────────────────────────────────────
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ─── 7) Train model ─────────────────────────────────────────────────────────────
model = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=50,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# ─── 8) Persist artifacts ──────────────────────────────────────────────────────
os.makedirs("model", exist_ok=True)
joblib.dump(model,    "model/difficulty_nn.pkl")
joblib.dump(scaler,   "model/difficulty_scaler.pkl")

# Save the full DataFrame (with 'name') for lookup in your API pipeline
joblib.dump(selected, "model/df_raw.pkl")

print("Preprocessing complete and artifacts saved to /model.")
