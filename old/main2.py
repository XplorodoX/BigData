#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import sys
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

def get_paginated_competitions(api, search_term):
    """
    Paginiert durch alle Wettbewerbe und gibt die vollständige Ergebnisliste zurück.
    """
    results = []
    page = 1
    while True:
        batch = api.competitions_list(search=search_term, page=page)
        if not batch:
            break
        results.extend(batch)
        page += 1
        time.sleep(1.2)
    return results

def get_paginated_notebooks(api, competition_ref):
    """
    Paginiert durch alle Notebooks für einen bestimmten Wettbewerb und gibt die vollständige Ergebnisliste zurück.
    """
    results = []
    page = 1
    while True:
        batch = api.kernels_list(
            competition=competition_ref,
            sort_by="dateCreated",
            page=page,
            page_size=100
        )
        if not batch:
            break
        results.extend(batch)
        page += 1
        time.sleep(1.2)
    return results

def download_notebook(api, kernel_ref, download_path):
    """
    Lädt ein Notebook herunter und speichert es im angegebenen Pfad.
    """
    try:
        api.kernels_pull(kernel_ref, path=download_path)
        return True
    except Exception as e:
        print(f"Fehler beim Herunterladen von '{kernel_ref}': {str(e)}")
        return False

def main():
    # Kaggle API initialisieren
    api = KaggleApi()
    api.authenticate()

    # Suchbegriff eingeben
    search_term = input("Suchbegriff für Wettbewerbe: ")

    print(f"Suche Wettbewerbe für '{search_term}'...")
    competitions = get_paginated_competitions(api, search_term)

    if not competitions:
        print("Keine Wettbewerbe gefunden.")
        sys.exit(0)

    print(f"Gefundene Wettbewerbe: {len(competitions)}\n")

    results = []
    for idx, comp in enumerate(competitions, start=1):
        try:
            title = comp.title if comp.title else comp.ref
            print(f"({idx}/{len(competitions)}) -> {title[:50]}...")

            # Verzeichnis für den Wettbewerb erstellen
            competition_dir = os.path.join("notebooks", comp.ref)
            os.makedirs(competition_dir, exist_ok=True)

            # Alle Notebooks für diesen Wettbewerb abfragen
            notebooks = get_paginated_notebooks(api, comp.ref)

            downloaded_count = 0
            for notebook in notebooks:
                kernel_ref = f"{notebook.ref}"
                if download_notebook(api, kernel_ref, competition_dir):
                    downloaded_count += 1

            results.append({
                "Competition": title,
                "ID": comp.ref,
                "Downloaded Notebooks": downloaded_count,
                "Total Notebooks": len(notebooks),
                "URL": f"https://kaggle.com/competitions/{comp.ref}"
            })

        except Exception as e:
            print(f"Fehler bei '{comp.ref}': {str(e)}")

    # Ergebnisse in DataFrame konvertieren
    df = pd.DataFrame(results)

    if df.empty:
        print("Keine Daten vorhanden, kann keine Auswertung erstellen.")
        sys.exit(0)

    df["Difference"] = df["Total Notebooks"] - df["Downloaded Notebooks"]

    # CSV exportieren
    csv_file = f"kaggle_notebook_counts_{search_term}.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')

    # Zusammenfassung ausgeben
    print("\nZusammenfassung:")
    print(df[["Competition", "Total Notebooks", "Downloaded Notebooks", "Difference"]])
    print(f"\nCSV exportiert: {csv_file}")

if __name__ == "__main__":
    main()
