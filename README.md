# Kaggle Competition Notebook Scraper

Dieses Repository enthält ein Python-Skript, das automatisch Kaggle-Notebooks zu bestimmten Wettbewerben abruft und in einer Excel-Datei speichert. Zudem sind hier begleitende Dateien wie ein wissenschaftliches Paper und eine `requirements.txt`-Datei für die Abhängigkeiten enthalten.

## 📌 Features
- Automatische Authentifizierung bei der Kaggle API
- Abruf der aktuellsten Notebooks für vorgegebene Kaggle-Wettbewerbe
- Speicherung der Notebook-Links mit zusätzlichen Metadaten in einer Excel-Datei
- Fehlerbehandlung für ungültige oder nicht zugängliche Wettbewerbe

## 📂 Projektstruktur
```
competition_notebook_scraper/
│── competition_notebook_links/  # Enthält die generierte Excel-Datei mit Notebook-Links
│── papers/                      # Enthält begleitende wissenschaftliche Paper
│   └── Seminararbeit_Big_Data_En.tex  # Wissenschaftliches Paper zum Projekt
│── README.md                    # Diese Datei
│── requirements.txt              # Abhängigkeiten für das Skript
│── scraper.py                    # Das Hauptskript
```

## 🚀 Installation & Nutzung
### 1️⃣ Voraussetzungen
- Ein Kaggle-Account
- Eine gültige `kaggle.json` API-Datei (muss im Verzeichnis `~/.kaggle/` oder in der Umgebungsvariable liegen)
- Python 3.8 oder höher

### 2️⃣ Installation
1. Klone das Repository:
   ```bash
   git clone https://github.com/dein-nutzername/competition_notebook_scraper.git
   cd competition_notebook_scraper
   ```
2. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

### 3️⃣ Nutzung
Führe das Skript aus, um die Notebooks abzurufen:
```bash
python scraper.py
```

Die generierte Excel-Datei wird im Ordner `competition_notebook_links/` gespeichert.

## 📝 Anpassungen
Falls du eigene Wettbewerbe durchsuchen möchtest, kannst du die `competitions_json`-Variable in `scraper.py` anpassen und die entsprechenden Slugs und URLs hinzufügen.

## 📜 Wissenschaftliches Paper
Das begleitende wissenschaftliche Paper **Seminararbeit_Big_Data_En.tex** befindet sich im Ordner `papers/`. Es dokumentiert die Methodik und die Ergebnisse dieses Projekts.

## 🔧 Fehlerbehandlung
- Falls ein Wettbewerb nicht existiert oder du keinen Zugriff hast, wird dies im Terminal angezeigt.
- Falls keine Notebooks für einen Wettbewerb gefunden werden, wird der Wettbewerb übersprungen.

## 📜 Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für weitere Details.

---
Made with ❤️ by [Dein Name]

