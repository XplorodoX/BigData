import os
import subprocess

# Wettbewerbe festlegen
competitions = ["playground-series-s4e12", "playground-series-s4e11", "equity-post-HCT-survival-predictions", "llms-you-cant-please-them-all", "santa-2024"]


# Funktion zum Herunterladen von Kernels eines Wettbewerbs
def download_kernels_for_competition(competition):
    # Spezifischen Ordner für den Wettbewerb erstellen
    competition_dir = os.path.join("kaggle_notebooks", competition)
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
