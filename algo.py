import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, SpectralClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load the Iris dataset
iris = load_iris()
X = iris.data
y_true = iris.target

# Standardize the dataset
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reduce dimensions for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Initialize clustering algorithms
algorithms = {
    "KMeans": KMeans(n_clusters=3, random_state=42),
    "DBSCAN": DBSCAN(eps=0.5, min_samples=5),
    "GaussianMixture": GaussianMixture(n_components=3, random_state=42),
    "AgglomerativeClustering": AgglomerativeClustering(n_clusters=3),
    "SpectralClustering": SpectralClustering(n_clusters=3, affinity='nearest_neighbors', random_state=42)
}

# Dictionary to store results
results = {}

# Apply each clustering algorithm and calculate silhouette scores
for name, algo in algorithms.items():
    if name == "GaussianMixture":
        labels = algo.fit_predict(X_scaled)
    else:
        labels = algo.fit_predict(X_scaled)

    silhouette_avg = silhouette_score(X_scaled, labels)
    results[name] = {
        "labels": labels,
        "silhouette_score": silhouette_avg
    }

    # Visualization
    plt.figure(figsize=(6, 4))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', s=50)
    plt.title(f"{name} (Silhouette: {silhouette_avg:.2f})")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.colorbar()
    plt.show()

# Print summary of silhouette scores
print("Clustering Algorithm Performance:")
for name, result in results.items():
    print(f"{name}: Silhouette Score = {result['silhouette_score']:.2f}")
