import json
import os
import subprocess

# JSON-Datei einlesen
json_file_path = "kaggle_wettbewerbe.json"  # Pfad zur JSON-Datei
try:
    with open(json_file_path, "r") as file:
        competitions_json = json.load(file)
except FileNotFoundError:
    print(f"Fehler: Die Datei '{json_file_path}' wurde nicht gefunden.")
    exit(1)
except json.JSONDecodeError:
    print(f"Fehler: Die Datei '{json_file_path}' enthält ungültiges JSON.")
    exit(1)

# Liste der Wettbewerbsnamen extrahieren
competitions = list(competitions_json.values())


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


# Für jeden Wettbewerb die Kernels herunterladen
for competition in competitions:
    print(f"Starte das Herunterladen der Kernels für den Wettbewerb: {competition}")
    download_kernels_for_competition(competition)
