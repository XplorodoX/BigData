# Kaggle-Wettbewerbsanalyse und Datenextraktion

Dieses Repository wurde im Rahmen des Big Data Seminars an der Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU) entwickelt. Es enthält Python-Skripte und JSON-Dateien zur Analyse von Kaggle-Wettbewerben, zur Datenextraktion und zum Organisieren von Jupyter-Notebooks. Das Projekt ist Teil einer Seminararbeit und bietet eine praktische Anwendung von Datenanalyse- und Extraktionstechniken.

## Inhaltsverzeichnis

1. [Überblick](#überblick)
2. [Dateien und Verzeichnisstruktur](#dateien-und-verzeichnisstruktur)
3. [Abhängigkeiten](#abhängigkeiten)
4. [Installation](#installation)
5. [Nutzung](#nutzung)
6. [Contributing](#contributing)
7. [Lizenz](#lizenz)

## Überblick

Dieses Projekt bietet Tools, um Daten von Kaggle-Wettbewerben zu analysieren und zu verarbeiten. Es umfasst Skripte zum Extrahieren, Sammeln und Verwalten von Daten sowie ein Beispiel-JSON für gespeicherte Wettbewerbsdaten. Ziel ist es, praktische Einblicke in die Herausforderungen und Lösungen im Bereich der Big Data Analyse zu vermitteln.

## Dateien und Verzeichnisstruktur

- **`algo.py`**: Enthält Algorithmen und Kernlogik.
- **`Collect_Notebooks.py`**: Ein Skript zum Sammeln und Organisieren von Jupyter-Notebooks.
- **`extract.py`**: Skript zur Datenextraktion aus JSON- oder anderen Quellen.
- **`kaggle_wettbewerbe.json`**: Eine JSON-Datei mit Links zu Kaggle-Wettbewerben und deren Kurzbezeichnungen.
- **`main.py`**: Hauptskript zur Initialisierung und Verwaltung des gesamten Workflows.

## Abhängigkeiten

Stelle sicher, dass folgende Python-Bibliotheken installiert sind:

- `pandas`
- `numpy`
- `requests`
- `json`
- `os`
- Weitere in den Skripten spezifizierte Abhängigkeiten

## Installation

1. Klone das Repository:
   ```bash
   git clone https://github.com/dein-username/kaggle-analyse.git
   ```
2. Navigiere ins Verzeichnis:
   ```bash
   cd kaggle-analyse
   ```
3. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

## Nutzung

1. **JSON-Datenanalyse**:
   - Öffne und bearbeite die Datei `kaggle_wettbewerbe.json`, um neue Wettbewerbe hinzuzufügen.
   
2. **Datenextraktion**:
   - Führe `extract.py` aus, um Daten aus JSON-Dateien oder APIs zu extrahieren:
     ```bash
     python extract.py
     ```

3. **Notebooks sammeln**:
   - Starte `Collect_Notebooks.py`, um Notebooks in einem Ordner zu organisieren:
     ```bash
     python Collect_Notebooks.py
     ```

4. **Kernlogik testen**:
   - Verwende `algo.py` für eigene Analysen oder Tests.

## Contributing

Beiträge sind willkommen! Bitte folge diesen Schritten:

1. Forke das Repository.
2. Erstelle einen neuen Branch:
   ```bash
   git checkout -b feature/DeinFeatureName
   ```
3. Nimm deine Änderungen vor und committe sie:
   ```bash
   git commit -m "Beschreibung der Änderungen"
   ```
4. Push den Branch:
   ```bash
   git push origin feature/DeinFeatureName
   ```
5. Erstelle einen Pull-Request.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die `LICENSE`-Datei für Details.

---