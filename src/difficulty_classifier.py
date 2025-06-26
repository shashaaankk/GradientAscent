import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import joblib

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
CSV_PATH = os.path.join("data", "output.csv")

# If you ever change the column order inside output.csv,
# update this list to match it exactly.
FEATURES = [
    "duration",
    "length_3d",
    "min_elevation",
    "max_elevation",
    "break_time",
    "uphill",
    "downhill",
]

from sklearn.neighbors import NearestNeighbors     # NEW import

def train_model(csv_path: str = CSV_PATH, n_clusters: int = 3):
    df = pd.read_csv(csv_path)
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(df[FEATURES])

    # ---------- K-Means (unchanged) ----------
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df["cluster"] = clusters

    cluster_order = (
        df.groupby("cluster")["duration"].mean().sort_values().index
    )
    labels = ["Easy", "Medium", "Hard"]
    cluster_map = {c: lbl for c, lbl in zip(cluster_order, labels)}

    # ---------- NEW: 5-NN model ----------
    nn = NearestNeighbors(n_neighbors=5, metric="euclidean")
    nn.fit(X_scaled)

    # Return everything you’ll need later
    return {
        "scaler":      scaler,
        "kmeans":      kmeans,
        "cluster_map": cluster_map,
        "nn":          nn,
        "X_scaled":    X_scaled,
        "df_raw":      df.reset_index(drop=True)  # keep original rows
    }

# ------------------------------------------------------------------
# INFERENCE
# ------------------------------------------------------------------
def predict_difficulty(row_df, artefacts):
    X_scaled = artefacts["scaler"].transform(row_df[FEATURES])
    cluster  = int(artefacts["kmeans"].predict(X_scaled)[0])
    label    = artefacts["cluster_map"][cluster]
    return label

def get_nearest_hikes(row_df, artefacts, n_neighbors=5):
    """
    Returns a DataFrame with the `n_neighbors` nearest rows from the
    original dataset, ordered by increasing distance.
    """
    X_scaled_query = artefacts["scaler"].transform(row_df[FEATURES])
    distances, indices = artefacts["nn"].kneighbors(X_scaled_query, n_neighbors=n_neighbors)
    out = artefacts["df_raw"].iloc[indices[0]].copy()
    out["distance"] = distances[0]
    return out.reset_index(drop=True)

# ------------------------------------------------------------------
# EXAMPLE USAGE
# ------------------------------------------------------------------
if __name__ == "__main__":
    artefacts = train_model()                      # one-off training

    new_hike = pd.DataFrame(
        [[5000, 7500, 400, 1600, 600, 1200, 1300]],
        columns=FEATURES
    )

    diff = predict_difficulty(new_hike, artefacts)
    print(f"Predicted cluster: {diff}")

    nearest5 = get_nearest_hikes(new_hike, artefacts)
    print("\nFive nearest hikes:\n", nearest5[["duration", "uphill", "downhill", "distance"]])



