import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import os

file_path = os.path.join("data", "output.csv")
df = pd.read_csv(file_path)

# Detect numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Prepare numeric data: assume cleaned, no NaNs
df_numeric = df[numeric_cols]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_numeric)

# Apply KMeans with k=3
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

# Fit NearestNeighbors on the scaled data
nn = NearestNeighbors(n_neighbors=5, metric='euclidean')
nn.fit(X_scaled)

def find_5_nearest(gpx_idx):
 
    if gpx_idx not in df.index:
        print(f"Index {gpx_idx} not found in DataFrame.")
        return
    pos = df.index.get_loc(gpx_idx)
    dist_arr, idx_arr = nn.kneighbors(X_scaled[pos].reshape(1, -1))
    dist_arr = dist_arr.flatten()
    idx_arr = idx_arr.flatten()
    neighbors = []
    for dist, pos_i in zip(dist_arr, idx_arr):
        idx_i = df.index[pos_i]
        if idx_i == gpx_idx:
            continue
        neighbors.append((idx_i, dist, df.at[idx_i, 'cluster']))
        if len(neighbors) >= 5:
            break
    print(f"\nQuery index: {gpx_idx}, Cluster: {df.at[gpx_idx, 'cluster']}")
    print("Query feature values:")
    print(df.loc[gpx_idx, numeric_cols].to_string())
    if neighbors:
        neigh_rows = []
        for neigh_idx, dist, cluster in neighbors:
            row_vals = {col: df.at[neigh_idx, col] for col in numeric_cols}
            row_vals.update({
                'neighbor_index': neigh_idx,
                'distance': dist,
                'cluster': cluster
            })
            neigh_rows.append(row_vals)
        neigh_df = pd.DataFrame(neigh_rows)
        cols = ['neighbor_index', 'cluster', 'distance'] + numeric_cols
        print("\n5 Nearest Neighbors:")
        print(neigh_df[cols].sort_values('distance').to_string(index=False))
    else:
        print("No neighbors found (data may have fewer rows).")

# Example: take a random row from df as input
sample_index = df.sample(n=1, random_state=42).index[0]
print(f"\nUsing random sample index from df: {sample_index}")
find_5_nearest(sample_index)