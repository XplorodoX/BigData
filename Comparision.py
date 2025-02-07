#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vergleich von fünf Clustering-Methoden

Dieses Skript liest alle CSV-Dateien aus einem angegebenen Ordner ein (z. B. aus
dem Kaggle-Dataset "Clustering Exercises"). Für jede Datei werden die folgenden
Clustering-Algorithmen angewandt:
    - KMeans
    - AgglomerativeClustering
    - SpectralClustering
    - GaussianMixture
    - BayesianGaussianMixture

Dabei wird zuerst geprüft, ob die Spalten 'x' und 'y' existieren (ansonsten werden
alle numerischen Spalten verwendet). Die Daten werden skaliert, danach wird
jedem Modell das Clustering zugeordnet, der Silhouette-Score berechnet und die
Ergebnisse werden in einem Plot visualisiert. Die Plots werden zusätzlich als PNG
gespeichert.
"""

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

# Klassische Clustering-Algorithmen
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering
# Probabilistische Modelle
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture


def load_and_preprocess(file_path):
    """
    Lädt eine CSV-Datei und wählt geeignete Features aus.

    Falls 'x' und 'y' vorhanden sind, werden diese genutzt; ansonsten werden
    alle numerischen Spalten herangezogen. Anschließend erfolgt eine Standardisierung.

    Parameter:
        file_path (str): Pfad zur CSV-Datei.

    Returns:
        data_scaled (ndarray): Skalierte Daten.
        df (DataFrame): Originaler DataFrame.
    """
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
    """
    Wendet das übergebene Clustering-Modell auf die Daten an und berechnet
    den Silhouette-Score.

    Einige Modelle (wie GaussianMixture) haben keine fit_predict()-Methode, daher
    wird hier zwischen fit_predict und fit/predict unterschieden.

    Parameter:
        model: Clustering-Modell.
        data (ndarray): Vorverarbeitete (skalierte) Daten.
        algorithm_name (str): Name des Algorithmus (für Ausgaben).

    Returns:
        labels (ndarray): Cluster-Zuweisungen.
        score (float): Silhouette-Score (oder None, falls nicht berechenbar).
    """
    if hasattr(model, "fit_predict"):
        labels = model.fit_predict(data)
    else:
        # Für Modelle wie GaussianMixture und BayesianGaussianMixture
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
            print(f"Fehler beim Berechnen des Silhouette-Scores für {algorithm_name}: {e}")
            score = None

    print(f"{algorithm_name}: {len(unique_labels)} Cluster, Silhouette-Score = {score}")
    return labels, score


def plot_clustering_results(data, labels_dict, silhouette_dict, file_name):
    """
    Visualisiert die Clustering-Ergebnisse aller Modelle in einem Plot.

    Falls die Dimensionen >2 betragen, wird mittels PCA auf 2 Dimensionen reduziert.
    Die Visualisierung erfolgt in einem Grid, dessen Größe sich dynamisch nach der
    Anzahl der Modelle richtet. Der Plot wird gespeichert.

    Parameter:
        data (ndarray): (ggf. reduzierte) Daten.
        labels_dict (dict): Dictionary, das jedem Modell Cluster-Labels zuordnet.
        silhouette_dict (dict): Dictionary, das jedem Modell den Silhouette-Score zuordnet.
        file_name (str): Name der aktuellen CSV-Datei (für Titel und Dateiname des Plots).
    """
    # Reduktion auf 2D, falls mehr als 2 Features vorliegen
    if data.shape[1] > 2:
        pca = PCA(n_components=2)
        data_2d = pca.fit_transform(data)
    else:
        data_2d = data

    algorithms = list(labels_dict.keys())
    n_algorithms = len(algorithms)
    n_cols = min(n_algorithms, 3)
    n_rows = math.ceil(n_algorithms / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 5 * n_rows))
    # Falls es nur einen Plot gibt oder wenn axes ein 2D-Array ist
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = np.array([axes])
    elif n_cols == 1:
        axes = np.array([[ax] for ax in axes])

    # Flache Liste der Achsen zum einfachen Durchlaufen
    axes_flat = axes.flatten()

    for idx, algo in enumerate(algorithms):
        ax = axes_flat[idx]
        labels = labels_dict[algo]
        score = silhouette_dict.get(algo, None)
        title = f"{algo}\nSilhouette: {score:.2f}" if score is not None else f"{algo}\nSilhouette: N/A"
        sns.scatterplot(x=data_2d[:, 0], y=data_2d[:, 1],
                        hue=labels, palette="viridis", ax=ax,
                        legend='full', s=50)
        ax.set_title(title)
        ax.set_xlabel("Komponente 1")
        ax.set_ylabel("Komponente 2")

    # Leere Subplots ausblenden
    for j in range(idx + 1, len(axes_flat)):
        fig.delaxes(axes_flat[j])

    plt.suptitle(f"Clustering Ergebnisse für: {os.path.basename(file_name)}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    output_file = f"clustering_result_{os.path.basename(file_name).split('.')[0]}.png"
    plt.savefig(output_file)
    print(f"Plot gespeichert als: {output_file}")
    plt.show()


def main():
    # Ordner, in dem sich die CSV-Dateien befinden (anpassen!)
    dataset_folder = "archive"  # Beispielordner
    csv_files = glob.glob(os.path.join(dataset_folder, "*.csv"))

    if not csv_files:
        print("Keine CSV-Dateien im angegebenen Verzeichnis gefunden.")
        return

    # Festlegung der Anzahl der Cluster bzw. Komponenten
    n_clusters = 3

    # Definition der fünf Modelle
    models = {
        "KMeans": KMeans(n_clusters=n_clusters, random_state=42),
        "Agglomerative": AgglomerativeClustering(n_clusters=n_clusters),
        "Spectral": SpectralClustering(n_clusters=n_clusters, random_state=42, affinity='nearest_neighbors'),
        "GaussianMixture": GaussianMixture(n_components=n_clusters, random_state=42),
        "BayesianGaussianMixture": BayesianGaussianMixture(n_components=n_clusters, random_state=42)
    }

    # Verarbeite jede CSV-Datei im Ordner
    for file_path in csv_files:
        print(f"\nVerarbeite Datei: {file_path}")
        data, df = load_and_preprocess(file_path)
        if data is None:
            continue

        labels_dict = {}
        silhouette_dict = {}

        for name, model in models.items():
            print(f"--- {name} ---")
            labels, score = perform_clustering(model, data, algorithm_name=name)
            labels_dict[name] = labels
            silhouette_dict[name] = score

        plot_clustering_results(data, labels_dict, silhouette_dict, file_path)


if __name__ == "__main__":
    main()
