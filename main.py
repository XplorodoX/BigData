import os
import nbformat
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
import numpy as np

CLUSTERING_ALGOS = [
    "KMeans", "DBSCAN", "AgglomerativeClustering", "SpectralClustering",
    "MeanShift", "AffinityPropagation", "Birch", "OPTICS", "GaussianMixture",
    "HierarchicalClustering", "FuzzyCMeans", "MiniBatchKMeans", "CanopyClustering",
    "SubspaceClustering", "SelfOrganizingMap", "KMedoids", "KPrototypes", "CLIQUE",
    "CURE", "Chameleon", "DENCLUE", "SNNClustering", "GMMClustering", "EMClustering",
    "HierarchicalAgglomerativeClustering", "DivisiveClustering", "DensityBasedClustering",
    "ModelBasedClustering", "GridBasedClustering", "CoClustering", "Biclustering",
    "SpectralBiclustering", "LatentClassAnalysis", "DBCLASD", "ROCKClustering",
    "WaveCluster", "STINGClustering", "OPTICSXi", "HDBSCAN", "SOMClustering",
    "NeuralGasClustering", "AffinityClustering", "LinkageClustering", "WardClustering",
    "SLINK", "CLINK", "NNChain", "AnderbergClustering", "LeaderClustering", "DeLiClu",
    "HiSC", "HiCO", "DiSH", "4CClustering", "ERiCClustering", "COPAC", "P3CClustering",
    "CASHClustering", "DOCClustering", "FastDOCClustering", "PAMClustering", "CLARAClustering",
    "CLARANSClustering", "FastPAM", "ApproximatePAM", "BalancedIterativeReducingClustering",
    "IterativeDichotomiser3", "C45Algorithm", "C50Algorithm", "CHAIDAlgorithm", "DecisionStump",
    "ConditionalDecisionTree", "RandomForest", "SLIQAlgorithm", "BayesianClustering",
    "NaiveBayesClustering", "GaussianNaiveBayesClustering", "MultinomialNaiveBayesClustering",
    "AODEClustering", "BayesianBeliefNetworkClustering", "BayesianNetworkClustering",
    "FisherDiscriminantClustering", "LinearRegressionClustering", "LogisticRegressionClustering",
    "MultinomialLogisticRegressionClustering", "PerceptronClustering", "SupportVectorMachineClustering",
    "SingleLinkageClustering", "CompleteLinkageClustering", "AverageLinkageClustering",
    "WardLinkageClustering", "CentroidLinkageClustering", "MedianLinkageClustering",
    "FlexibleLinkageClustering", "WeightedLinkageClustering", "UnweightedLinkageClustering",
    "UPGMAClustering", "WPGMAClustering", "UPGMCClustering", "WPGMCClustering", "DendrogramClustering",
    "AgglomerativeHierarchicalClustering", "DivisiveHierarchicalClustering", "DensityBasedSpatialClustering",
    "DensityBasedClustering", "ModelBasedClustering", "GridBasedClustering", "SubspaceClustering",
    "CoClustering", "Biclustering", "SpectralBiclustering", "LatentClassAnalysis", "DBCLASD",
    "ROCKClustering", "WaveCluster", "STINGClustering"
]

def search_notebooks_in_competitions(main_folder):
    """Durchsucht alle Wettbewerbe und ihre Notebooks nach Clustering-Algorithmen."""
    results = {}

    for competition_name in os.listdir(main_folder):
        competition_path = os.path.join(main_folder, competition_name)
        if not os.path.isdir(competition_path):
            continue

        competition_results = {}

        for file_name in os.listdir(competition_path):
            if file_name.endswith(".ipynb"):
                file_path = os.path.join(competition_path, file_name)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        notebook = nbformat.read(f, as_version=4)

                    found_algos = set()
                    for cell in notebook.cells:
                        if cell.cell_type == "code":
                            cell_content = cell.source
                            for algo in CLUSTERING_ALGOS:
                                if algo in cell_content:
                                    found_algos.add(algo)

                    if found_algos:
                        competition_results[file_name] = list(found_algos)
                except Exception as e:
                    print(f"Fehler beim Lesen von {file_name}: {e}")

        if competition_results:
            results[competition_name] = competition_results

    return results

def save_results_to_csv(results, output_file="clustering_algorithms_report.csv"):
    """Speichert die Ergebnisse in einer CSV-Datei."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Wettbewerb", "Notebook", "Algorithmus"])
        for competition, notebooks in results.items():
            for notebook, algos in notebooks.items():
                for algo in algos:
                    writer.writerow([competition, notebook, algo])
    print(f"Ergebnisse gespeichert in: {output_file}")

def visualize_results_combined(results):
    """Visualisiert die gefundenen Clustering-Algorithmen mit Wettbewerben als Balken und Algorithmen als Farben."""
    algo_counts_by_competition = defaultdict(lambda: defaultdict(int))

    for competition, notebooks in results.items():
        for algos in notebooks.values():
            for algo in algos:
                algo_counts_by_competition[competition][algo] += 1

    # Vorbereitung der Daten
    competitions = list(algo_counts_by_competition.keys())
    algos = sorted(set(algo for comp in algo_counts_by_competition.values() for algo in comp))

    data = np.zeros((len(competitions), len(algos)))
    for i, competition in enumerate(competitions):
        for j, algo in enumerate(algos):
            data[i, j] = algo_counts_by_competition[competition][algo]

    # Visualisierung
    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.8 / len(algos)
    indices = np.arange(len(competitions))

    for j, algo in enumerate(algos):
        ax.bar(indices + j * bar_width, data[:, j], bar_width, label=algo)

    ax.set_xticks(indices + bar_width * (len(algos) - 1) / 2)
    ax.set_xticklabels(competitions, rotation=45, ha="right")
    ax.set_ylabel("Anzahl der Vorkommen")
    ax.set_title("Häufigkeit der Clustering-Algorithmen pro Wettbewerb")
    ax.legend(title="Clustering-Algorithmen")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Hauptordner mit Wettbewerben eingeben
    main_folder_path = "/Users/merluee/PycharmProjects/BigData/kaggle_notebooks"

    # Suche ausführen
    results = search_notebooks_in_competitions(main_folder_path)

    # Ergebnisse speichern
    save_results_to_csv(results)

    # Ergebnisse visualisieren
    if results:
        visualize_results_combined(results)
    else:
        print("Keine Clustering-Algorithmen in den Notebooks gefunden.")
