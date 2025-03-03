import os                      # Modul zur Arbeit mit Betriebssystempfaden
import glob                    # Modul zur Suche nach Dateien in Verzeichnissen
import math                    # Mathematische Funktionen (wird hier nicht aktiv genutzt)
import numpy as np             # Bibliothek für numerische Berechnungen
import pandas as pd            # Bibliothek zur Datenmanipulation und -analyse
import matplotlib.pyplot as plt  # Plotting-Bibliothek
import seaborn as sns          # Erweiterte Visualisierungsbibliothek

# Import von Funktionen und Klassen aus scikit-learn für Vorverarbeitung, Dimensionalitätsreduktion,
# Clustering und Evaluierung der Ergebnisse
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Importieren verschiedener Clustering-Algorithmen
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture

def load_and_preprocess(file_path):
    """
    Lädt eine CSV-Datei und führt die Vorverarbeitung der Daten durch.
    
    Schritte:
    1. Versucht, die CSV-Datei einzulesen. Bei einem Fehler wird eine entsprechende Meldung ausgegeben.
    2. Überprüft, ob die Spalten 'x' und 'y' vorhanden sind. Falls ja, werden diese verwendet,
       ansonsten werden alle numerischen Spalten ausgewählt.
    3. Falls keine numerischen Daten vorhanden sind, wird eine Fehlermeldung ausgegeben.
    4. Die ausgewählten Daten werden mittels StandardScaler normiert.
    
    Rückgabe:
    - data_scaled: Die skalierten Daten (als numpy Array)
    - df: Das ursprüngliche DataFrame (zur eventuellen weiteren Verwendung)
    """
    try:
        df = pd.read_csv(file_path)  # Einlesen der CSV-Datei
    except Exception as e:
        print(f"Fehler beim Laden der Datei {file_path}: {e}")
        return None, None

    # Auswahl der Spalten: Falls 'x' und 'y' vorhanden sind, werden diese genutzt
    if 'x' in df.columns and 'y' in df.columns:
        data = df[['x', 'y']]
    else:
        # Falls nicht, werden alle numerischen Spalten verwendet
        data = df.select_dtypes(include=[np.number])

    # Überprüfung, ob numerische Daten vorhanden sind
    if data.empty:
        print(f"Keine numerischen Daten in Datei {file_path}.")
        return None, df

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)  # Normierung der Daten
    return data_scaled, df

def perform_clustering(model, data, algorithm_name=""):
    """
    Führt das Clustering mit dem angegebenen Modell durch.
    
    Vorgehen:
    1. Überprüft, ob das Modell über die Methode 'fit_predict' verfügt und nutzt diese,
       ansonsten werden 'fit' und 'predict' getrennt aufgerufen.
    2. Bestimmt die Anzahl der Cluster, indem die eindeutigen Label ermittelt werden.
    3. Berechnet den Silhouette-Score, sofern mehr als ein Cluster gefunden wurde.
    4. Gibt die Cluster-Labels und den berechneten Silhouette-Score zurück.
    """
    if hasattr(model, "fit_predict"):
        labels = model.fit_predict(data)
    else:
        model.fit(data)
        labels = model.predict(data)

    unique_labels = np.unique(labels)  # Bestimmen der einzigartigen Cluster-Labels
    if len(unique_labels) < 2:
        score = None
        print(f"{algorithm_name}: Es wurden nur {len(unique_labels)} Cluster gefunden!")
    else:
        try:
            score = silhouette_score(data, labels)  # Berechnung des Silhouette-Scores
        except Exception as e:
            print(f"Fehler bei Berechnen des Silhouette-Scores für {algorithm_name}: {e}")
            score = None

    print(f"{algorithm_name}: {len(unique_labels)} Cluster, Silhouette-Score = {score}")
    return labels, score

def plot_and_save_clustering(data, labels, algorithm_name, silhouette_score, file_name):
    """
    Erstellt einen Scatterplot der Clustering-Ergebnisse und speichert diesen als PDF.
    
    Vorgehen:
    1. Falls die Daten mehr als 2 Dimensionen haben, wird PCA eingesetzt, um sie auf 2 Dimensionen zu reduzieren.
    2. Es wird ein Scatterplot erstellt, bei dem die Farben der Punkte den Clusterzugehörigkeiten entsprechen.
    3. Der Plot wird mit einem Titel versehen, der den Algorithmusnamen und den Silhouette-Score anzeigt.
    4. Der Plot wird als PDF-Datei gespeichert, wobei der Dateiname den Namen des Algorithmus und der
       Ursprungsdatei enthält.
    """
    # Reduktion der Daten auf 2 Dimensionen, falls nötig
    if data.shape[1] > 2:
        pca = PCA(n_components=2)
        data_2d = pca.fit_transform(data)
    else:
        data_2d = data

    plt.figure(figsize=(6, 5))
    sns.scatterplot(x=data_2d[:, 0], y=data_2d[:, 1], hue=labels, palette="viridis", legend='full', s=50)
    # Formatierung des Titels, abhängig davon, ob ein Silhouette-Score berechnet werden konnte
    title = f"{algorithm_name}\nSilhouette: {silhouette_score:.2f}" if silhouette_score is not None else f"{algorithm_name}\nSilhouette: N/A"
    plt.title(title)
    plt.xlabel("Komponente 1")
    plt.ylabel("Komponente 2")

    # Erstellen eines aussagekräftigen Dateinamens für den gespeicherten Plot
    output_file = f"clustering_result_{algorithm_name}_{os.path.basename(file_name).split('.')[0]}.pdf"
    plt.savefig(output_file, format='pdf')
    print(f"Plot gespeichert als: {output_file}")
    plt.close()

def main():
    """
    Hauptfunktion des Skripts:
    
    1. Sucht im Verzeichnis 'archive' nach CSV-Dateien.
    2. Für jede gefundene CSV-Datei:
       - Laden und Vorverarbeiten der Daten.
       - Anwenden verschiedener Clustering-Algorithmen (KMeans, Agglomerative, Spectral, 
         GaussianMixture, BayesianGaussianMixture) mit festgelegter Clusterzahl.
       - Berechnung des Silhouette-Scores zur Bewertung der Clusterqualität.
       - Visualisierung und Speicherung der Ergebnisse als PDF.
    """
    dataset_folder = "archive"
    csv_files = glob.glob(os.path.join(dataset_folder, "*.csv"))

    if not csv_files:
        print("Keine CSV-Dateien im angegebenen Verzeichnis gefunden.")
        return

    n_clusters = 3  # Festlegen der Anzahl der Cluster für die Analyse

    # Definition der verschiedenen Clustering-Modelle mit den jeweiligen Parametern
    models = {
        "KMeans": KMeans(n_clusters=n_clusters, random_state=42),
        "Agglomerative": AgglomerativeClustering(n_clusters=n_clusters),
        "Spectral": SpectralClustering(n_clusters=n_clusters, random_state=42, affinity='nearest_neighbors'),
        "GaussianMixture": GaussianMixture(n_components=n_clusters, random_state=42),
        "BayesianGaussianMixture": BayesianGaussianMixture(n_components=n_clusters, random_state=42)
    }

    # Iteration über alle gefundenen CSV-Dateien
    for file_path in csv_files:
        print(f"\nVerarbeite Datei: {file_path}")
        data, df = load_and_preprocess(file_path)
        if data is None:
            continue

        # Ausführen jedes Clustering-Modells auf den aktuellen Datensatz
        for name, model in models.items():
            print(f"--- {name} ---")
            labels, score = perform_clustering(model, data, algorithm_name=name)
            plot_and_save_clustering(data, labels, name, score, file_path)

# Ausführung des Skripts, falls es direkt aufgerufen wird
if __name__ == "__main__":
    main()
