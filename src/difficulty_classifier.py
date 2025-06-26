import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D projection)
import seaborn as sns

def visualize_PCA(X,kmeans):
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X)

    # Get cluster labels (from KMeans)
    clusters = kmeans.labels_

    # Plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Use seaborn color palette
    palette = sns.color_palette("Set2", 3)

    # Plot each cluster in a different color
    for cluster_id in range(3):
        mask = clusters == cluster_id
        ax.scatter(
            X_pca[mask, 0], X_pca[mask, 1], X_pca[mask, 2],
            label=f"Cluster {cluster_id}", color=palette[cluster_id], s=40
        )

    ax.set_title("3D Scatter Plot of Hiking Data Clusters")
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    ax.set_zlabel("PCA 3")
    ax.legend()
    plt.tight_layout()
    plt.show()

def visualize_3D_clusters(X, kmeans):
    """
    Visualizes 3D clustering results using the original 3D features in X.
    
    Parameters:
        X (DataFrame or ndarray): Input data with exactly 3 columns.
        kmeans (KMeans): Fitted KMeans model with `.labels_`.
    """
    # Convert to NumPy array if it's a DataFrame
    X_np = X.values if hasattr(X, "values") else X
    clusters = kmeans.labels_

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    palette = sns.color_palette("Set2", np.unique(clusters).max() + 1)

    for cluster_id in np.unique(clusters):
        mask = clusters == cluster_id
        ax.scatter(
            X_np[mask, 0], X_np[mask, 1], X_np[mask, 2],
            label=f"Cluster {cluster_id}", color=palette[cluster_id], s=40
        )

    ax.set_title("3D Scatter Plot of Clusters")
    ax.set_xlabel("length_3d")
    ax.set_ylabel("max_elevation")
    ax.set_zlabel("break_time")
    ax.legend()
    plt.tight_layout()
    plt.show()

def main():
    #selected = df[["duration","length_3d", "min_elevation", "max_elevation", "break_time", "uphill", "downhill"]]
    csv_path = os.path.join("data", "output.csv")
    df = pd.read_csv(csv_path)
    print(df.head())
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(df)

    # Add the cluster labels to your DataFrame
    X_clustered = pd.DataFrame(df, columns=df.columns)
    X_clustered["difficulty_cluster"] = clusters

    #visualize_PCA(df,kmeans)
    visualize_3D_clusters(df[["length_3d","max_elevation","duration"]],kmeans)
    # Optional: Save to CSV
    # X_clustered.to_csv("clustered_difficulty.csv", index=False)

    print(X_clustered["difficulty_cluster"].value_counts())
if __name__ == "__main__":
    main()

