# Vergleich von häufigsten Clustering-Algorithmen auf Kaggle

Dieses Repository enthält den Quellcode sowie alle begleitenden Materialien zur Seminararbeit *"Vergleich von häufigsten Clustering-Algorithmen auf Kaggle"* von Florian Merlau. Die Arbeit entstand im Rahmen des Big Data Seminars (WS 2024/2025) an der Friedrich-Alexander-Universität Erlangen-Nürnberg.

## Überblick

Die Seminararbeit untersucht systematisch den Einsatz und die Performance gängiger Clustering-Algorithmen in Kaggle-Wettbewerben. Im Fokus stehen unter anderem:

- **K-Means**
- **Agglomerative Clustering**
- **Spectral Clustering**
- **Gaussian Mixture Models (GMM)**
- **Bayesian Gaussian Mixture Models (BGMM)**

Es wird analysiert, welche Algorithmen in der Praxis am häufigsten eingesetzt werden und wie sie sich in unterschiedlichen Szenarien – von klar abgegrenzten Clustern bis zu komplexen, nicht-konvexen Strukturen – verhalten.

## Repository-Struktur

- **Seminararbeit_Big_Data.pdf**  
  Vollständiger Bericht der Seminararbeit.

- **/src**  
  Python-Skripte zur automatisierten Erfassung, Analyse und Aufbereitung der Daten aus Kaggle-Wettbewerben.

- **/data**  
  Beispieldatensätze, generierte Excel-Dateien und weitere Analysedaten.

- **/notebooks**  
  Jupyter Notebooks zur Visualisierung der Ergebnisse und zur explorativen Analyse.

## Voraussetzungen

- **Python 3.x**
- Notwendige Bibliotheken (siehe `requirements.txt`):  
  `pandas`, `numpy`, `matplotlib`, `kaggle` (API) und weitere.
- (Optional) Ein gültiger Kaggle API-Key, um Notebooks und Wettbewerbsdaten automatisiert abzurufen.

## Installation

1. **Repository klonen:**
    ```bash
    git clone https://github.com/XplorodoX/BigData.git
    ```

2. **In das Repository-Verzeichnis wechseln:**
    ```bash
    cd BigData
    ```

3. **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

4. **(Optional) Kaggle API konfigurieren:**  
   Erstelle eine Datei namens `kaggle.json` mit deinen API-Anmeldedaten und platziere sie im Verzeichnis `~/.kaggle/`.

## Nutzung

- **Datenabruf und Analyse:**  
  Führe das Skript `src/fetch_and_analyze.py` aus, um Notebooks von Kaggle abzurufen und die Daten zu analysieren:
  ```bash
  python src/fetch_and_analyze.py
