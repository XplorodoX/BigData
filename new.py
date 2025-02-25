import os
import glob
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture

def load_and_preprocess(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Fehler beim Laden der Datei {file_path}: {e}")
        return None, None

    if 'x' in df.columns and 'y' in df.columns:
        data = df[['x', 'y']]
    else:
        data = df.select_dtypes(include=[np.number])

    if data.empty:
        print(f"Keine numerischen Daten in Datei {file_path}.")
        return None, df

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    return data_scaled, df

def perform_clustering(model, data, algorithm_name=""):
    if hasattr(model, "fit_predict"):
        labels = model.fit_predict(data)
    else:
        model.fit(data)
        labels = model.predict(data)

    unique_labels = np.unique(labels)
    if len(unique_labels) < 2:
        score = None
        print(f"{algorithm_name}: Es wurden nur {len(unique_labels)} Cluster gefunden!")
    else:
        try:
            score = silhouette_score(data, labels)
        except Exception as e:
            print(f"Fehler bei Berechnen des Silhouette-Scores für {algorithm_name}: {e}")
            score = None

    print(f"{algorithm_name}: {len(unique_labels)} Cluster, Silhouette-Score = {score}")
    return labels, score

def plot_and_save_clustering(data, labels, algorithm_name, silhouette_score, file_name):
    if data.shape[1] > 2:
        pca = PCA(n_components=2)
        data_2d = pca.fit_transform(data)
    else:
        data_2d = data

    plt.figure(figsize=(6, 5))
    sns.scatterplot(x=data_2d[:, 0], y=data_2d[:, 1], hue=labels, palette="viridis", legend='full', s=50)
    title = f"{algorithm_name}\nSilhouette: {silhouette_score:.2f}" if silhouette_score is not None else f"{algorithm_name}\nSilhouette: N/A"
    plt.title(title)
    plt.xlabel("Komponente 1")
    plt.ylabel("Komponente 2")

    output_file = f"clustering_result_{algorithm_name}_{os.path.basename(file_name).split('.')[0]}.pdf"
    plt.savefig(output_file, format='pdf')
    print(f"Plot gespeichert als: {output_file}")
    plt.close()

def main():
    dataset_folder = "archive"
    csv_files = glob.glob(os.path.join(dataset_folder, "*.csv"))

    if not csv_files:
        print("Keine CSV-Dateien im angegebenen Verzeichnis gefunden.")
        return

    n_clusters = 3

    models = {
        "KMeans": KMeans(n_clusters=n_clusters, random_state=42),
        "Agglomerative": AgglomerativeClustering(n_clusters=n_clusters),
        "Spectral": SpectralClustering(n_clusters=n_clusters, random_state=42, affinity='nearest_neighbors'),
        "GaussianMixture": GaussianMixture(n_components=n_clusters, random_state=42),
        "BayesianGaussianMixture": BayesianGaussianMixture(n_components=n_clusters, random_state=42)
    }

    for file_path in csv_files:
        print(f"\nVerarbeite Datei: {file_path}")
        data, df = load_and_preprocess(file_path)
        if data is None:
            continue

        for name, model in models.items():
            print(f"--- {name} ---")
            labels, score = perform_clustering(model, data, algorithm_name=name)
            plot_and_save_clustering(data, labels, name, score, file_path)

if __name__ == "__main__":
    main()