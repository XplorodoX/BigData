import json
import os
import subprocess
import shutil
import random

# JSON-Datei einlesen
json_file_path = "kaggle_wettbewerbe.json"  # Pfad zur JSON-Datei
try:
    with open(json_file_path, "r") as file:
        competitions_json = json.load(file)
        # Extrahiere die Wettbewerbsnamen aus den JSON-Schlüsseln
        competitions = [value for key, value in competitions_json.items()]
        if not competitions:
            print("Fehler: Keine Wettbewerbe in der Datei gefunden.")
            exit(1)
except FileNotFoundError:
    print(f"Fehler: Die Datei '{json_file_path}' wurde nicht gefunden.")
    exit(1)
except json.JSONDecodeError:
    print(f"Fehler: Die Datei '{json_file_path}' enthält ungültiges JSON.")
    exit(1)


# Funktion zum Herunterladen von Kernels eines Wettbewerbs
def download_kernels_for_competition(competition):
    # Spezifischen Ordner für den Wettbewerb erstellen
    competition_dir = os.path.join("kaggle_notebooks", competition)

    # Überprüfen, ob der Ordner bereits existiert
    if os.path.exists(competition_dir):
        print(f"Überspringe {competition}: Ordner '{competition_dir}' existiert bereits.")
        return

    os.makedirs(competition_dir, exist_ok=True)

    try:
        # 1. Liste aller Kernels für diesen Wettbewerb abrufen
        kernels_output = subprocess.check_output([
            "kaggle", "kernels", "list", "--competition", competition,
            "--page-size", "10000", "--csv"
        ], universal_newlines=True)

        # Die Ausgabe ist CSV-formatiert. Die erste Zeile ist Header.
        lines = kernels_output.strip().split("\n")
        headers = lines[0].split(",")
        slug_index = headers.index("ref")

        # Jede weitere Zeile enthält Details zu einem Kernel
        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) <= slug_index:
                continue

            kernel_ref = parts[slug_index]
            # kernel_ref hat typischerweise ein Format wie: "username/kernel-slug"
            # Herunterladen des Kernels:
            try:
                subprocess.run(["kaggle", "kernels", "pull", kernel_ref, "-p", competition_dir], check=True)
                print(f"Heruntergeladen: {kernel_ref}")
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Herunterladen von {kernel_ref}: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Abrufen der Kernel-Liste für {competition}: {e}")


# Funktion, um 1% der Dateien in einen neuen Ordner zu kopieren
def copy_sample_files(competition):
    source_dir = os.path.join("kaggle_notebooks", competition)
    sample_dir = os.path.join("kaggle_samples", competition)

    if not os.path.exists(source_dir):
        print(f"Fehler: Quellordner '{source_dir}' existiert nicht.")
        return

    os.makedirs(sample_dir, exist_ok=True)

    # Alle Dateien im Ordner auflisten
    all_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if
                 os.path.isfile(os.path.join(source_dir, f))]

    if not all_files:
        print(f"Keine Dateien im Ordner '{source_dir}' gefunden.")
        return

    # 1% der Dateien auswählen
    sample_size = max(1, len(all_files) // 100)  # Mindestens 1 Datei
    sample_files = random.sample(all_files, sample_size)

    # Dateien in den neuen Ordner kopieren
    for file in sample_files:
        shutil.copy(file, sample_dir)
        print(f"Kopiert: {file} -> {sample_dir}")


# Für jeden Wettbewerb die Kernels herunterladen und 1% in den Sample-Ordner kopieren
for competition in competitions:
    print(f"Starte das Herunterladen der Kernels für den Wettbewerb: {competition}")
    download_kernels_for_competition(competition)
    print(f"Kopiere 1% der Dateien für den Wettbewerb: {competition}")
    copy_sample_files(competition)
