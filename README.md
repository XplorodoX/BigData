# Vergleich von häufigsten Clustering-Algorithmen auf Kaggle

Willkommen in diesem Repository! Hier findest du den Quellcode sowie alle begleitenden Materialien zur Seminararbeit *„Vergleich von häufigsten Clustering-Algorithmen auf Kaggle“* von Florian Merlau. Die Arbeit entstand im Rahmen des Big Data Seminars (WS 2024/2025) an der Friedrich-Alexander-Universität Erlangen-Nürnberg.

---

## Überblick

Die Seminararbeit untersucht den Einsatz und die Performance gängiger Clustering-Algorithmen in Kaggle-Wettbewerben. Der Fokus liegt auf folgenden Verfahren:

- **K-Means**  
- **Agglomerative Clustering**  
- **Spectral Clustering**  
- **Gaussian Mixture Models (GMM)**  
- **Bayesian Gaussian Mixture Models (BGMM)**  

Anhand öffentlich verfügbarer Kaggle-Notebooks wird analysiert, welche Algorithmen am häufigsten genutzt werden und wie sie sich bei unterschiedlich strukturierten Datensätzen (z. B. klar abgegrenzte Cluster vs. komplexe, nicht-konvexe Strukturen) verhalten.

---

## Repository-Struktur

- **Seminararbeit_Big_Data.pdf**  
  Enthält die vollständige Ausarbeitung (Seminararbeit).

- **/src**  
  Python-Skripte zur automatisierten Erfassung, Analyse und Aufbereitung der Daten aus Kaggle-Wettbewerben.

- **/data**  
  Beispieldatensätze, generierte Excel-Dateien und weitere Analyseergebnisse.

- **/notebooks**  
  Jupyter Notebooks zur interaktiven Visualisierung und Exploration der Ergebnisse.

---

## Voraussetzungen

- **Python 3.x**
- Installation der in `requirements.txt` aufgeführten Bibliotheken (z. B. `pandas`, `numpy`, `matplotlib`, `kaggle`):
  ```bash
  pip install -r requirements.txt
  ```
- (Optional) Ein gültiger **Kaggle API-Key**, um Wettbewerbsdaten automatisiert abzurufen.  
  (Details zur Einrichtung siehe [Kaggle API-Dokumentation](https://github.com/Kaggle/kaggle-api))

---

## Installation

1. **Repository klonen**  
   ```bash
   git clone https://github.com/XplorodoX/BigData.git
   ```
2. **In das Projektverzeichnis wechseln**  
   ```bash
   cd BigData
   ```
3. **Abhängigkeiten installieren**  
   ```bash
   pip install -r requirements.txt
   ```
4. **(Optional) Kaggle API konfigurieren**  
   - Erstelle eine Datei namens `kaggle.json` mit deinen API-Zugangsdaten.  
   - Platziere sie unter `~/.kaggle/` (Linux/Mac) oder `%USERPROFILE%\.kaggle\` (Windows).

---

## Nutzung

- **Datenabruf und Analyse**  
  Führe das Skript `src/fetch_and_analyze.py` aus, um Kaggle-Notebooks zu durchsuchen und relevante Daten zu extrahieren:
  ```bash
  python src/fetch_and_analyze.py
  ```
  Anschließend werden die Ergebnisse (z. B. Excel-Dateien mit Übersicht zu den verwendeten Algorithmen) im Ordner **/data** abgelegt.

- **Visualisierung und Exploration**  
  In den Jupyter Notebooks unter **/notebooks** kannst du die Ergebnisse interaktiv auswerten und verschiedene Diagramme oder Metriken betrachten.

---

## Ergebnisse

Die Analyse zeigt u. a., dass **K-Means** in Kaggle-Notebooks besonders häufig genutzt wird – wahrscheinlich aufgrund seiner einfachen Implementierung und schnellen Rechenzeiten. Bei komplexeren Datensätzen oder Ausreißern können jedoch andere Algorithmen wie **Spectral Clustering** oder **GMM/BGMM** im Vorteil sein.

---

## Mitwirken

Beiträge, Verbesserungsvorschläge und Fehlerkorrekturen sind jederzeit willkommen!  
- **Issues** eröffnen bei Problemen oder neuen Ideen.  
- **Pull Requests** erstellen, um Änderungen vorzuschlagen.

---

## Lizenz

Sofern nicht anders angegeben, steht dieses Projekt unter der [MIT Lizenz](LICENSE). Bitte beachte gegebenenfalls zusätzliche Lizenzhinweise in den jeweiligen Unterordnern oder Dateien.

---

**Autor:**  
[Florian Merlau](mailto:florian.merlau@fau.de)  
Friedrich-Alexander-Universität Erlangen-Nürnberg, Big Data Seminar WS 2024/2025
