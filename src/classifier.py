import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import joblib

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
CSV_PATH = os.path.join("data", "output.csv")
ARTIFACT_DIR = "model"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# If you ever change the column order inside output.csv,
# update this list to match it exactly.
FEATURES = [
    "length_3d",
    "min_elevation",
    "max_elevation",
    "uphill",
    "downhill",
    "break_time",
    "duration"
]

# Paths for serialized difficulty artifacts
DIFF_SCALER_PATH = os.path.join(ARTIFACT_DIR, "difficulty_scaler.pkl")
DIFF_KMEANS_PATH = os.path.join(ARTIFACT_DIR, "difficulty_kmeans.pkl")
DIFF_MAP_PATH    = os.path.join(ARTIFACT_DIR, "difficulty_cluster_map.pkl")
DIFF_NN_PATH     = os.path.join(ARTIFACT_DIR, "difficulty_nn.pkl")
DIFF_DF_RAW_PATH = os.path.join(ARTIFACT_DIR, "difficulty_df_raw.pkl")


def train_model(csv_path: str = CSV_PATH, n_clusters: int = 3):
    """
    Train KMeans clustering and a 5-NN model on hike features,
    then serialize all artifacts to disk.
    """
    # Load data
    df = pd.read_csv(csv_path)

    # Fit scaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(df[FEATURES])

    # Train KMeans and assign clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df["cluster"] = clusters

    # Map cluster IDs to labels by average duration
    cluster_order = df.groupby("cluster")["duration"].mean().sort_values().index
    labels = ["Easy", "Medium", "Hard"]
    cluster_map = {cid: lbl for cid, lbl in zip(cluster_order, labels)}

    # Train NearestNeighbors for retrieval
    nn = NearestNeighbors(n_neighbors=5, metric="euclidean")
    nn.fit(X_scaled)

    # Serialize individual artifacts
    joblib.dump(scaler, DIFF_SCALER_PATH)
    joblib.dump(kmeans, DIFF_KMEANS_PATH)
    joblib.dump(cluster_map, DIFF_MAP_PATH)
    joblib.dump(nn, DIFF_NN_PATH)
    joblib.dump(df.reset_index(drop=True), DIFF_DF_RAW_PATH)

    print("Saved difficulty artifacts to model folder:")
    print(f"  Scaler -> {DIFF_SCALER_PATH}")
    print(f"  KMeans -> {DIFF_KMEANS_PATH}")
    print(f"  Map    -> {DIFF_MAP_PATH}")
    print(f"  5NN    -> {DIFF_NN_PATH}")
    print(f"  RawDF  -> {DIFF_DF_RAW_PATH}")

    return {
        "scaler":      scaler,
        "kmeans":      kmeans,
        "cluster_map": cluster_map,
        "nn":          nn,
        "df_raw":      df.reset_index(drop=True)
    }


def predict_difficulty(row_df, artefacts):
    """
    Predict difficulty label for given hike features DataFrame.
    """
    X_scaled = artefacts["scaler"].transform(row_df[FEATURES])
    cluster  = artefacts["kmeans"].predict(X_scaled)[0]
    return artefacts["cluster_map"][cluster]


def get_nearest_hikes(row_df, artefacts, n_neighbors: int = 5):
    """
    Return the nearest n_neighbors hikes from the original data,
    ordered by increasing distance in feature space.
    """
    X_scaled = artefacts["scaler"].transform(row_df[FEATURES])
    distances, indices = artefacts["nn"].kneighbors(X_scaled, n_neighbors=n_neighbors)
    neigh_df = artefacts["df_raw"].iloc[indices[0]].copy()
    neigh_df["distance"] = distances[0]
    return neigh_df.reset_index(drop=True)


if __name__ == "__main__":
    # Train and save artifacts
    artefacts = train_model()

    # Example usage
    new_hike = pd.DataFrame(
        [[5000, 7500, 400, 1600, 600, 1200, 1300]],
        columns=FEATURES
    )

    diff = predict_difficulty(new_hike, artefacts)
    print(f"Predicted difficulty: {diff}")

    nearest5 = get_nearest_hikes(new_hike, artefacts)
    print("\nFive nearest hikes:\n", nearest5[["duration", "uphill", "downhill", "distance"]])
