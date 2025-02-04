import os
import random
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.rest import ApiException

# Kaggle-API authentifizieren
api = KaggleApi()
api.authenticate()

# JSON-Daten mit den Links und Slugs
competitions_json = {
    "https://www.kaggle.com/competitions/manufacturer-name-clustering": "manufacturer-name-clustering",
    "https://www.kaggle.com/competitions/dmassign1": "dmassign1",
    "https://www.kaggle.com/competitions/bigdata-and-datamining-2nd-ex": "bigdata-and-datamining-2nd-ex",
    "https://www.kaggle.com/competitions/tabular-playground-series-jul-2022": "tabular-playground-series-jul-2022",
    "https://www.kaggle.com/competitions/physical-activity-clustering": "physical-activity-clustering"
}

# Ordner, in dem die Excel-Datei landen soll
output_dir = "competition_notebook_links"
os.makedirs(output_dir, exist_ok=True)

# Hier sammeln wir alle Daten, um sie später in einem Rutsch in Excel zu schreiben
excel_rows = []

if not competitions_json:
    print("Keine Wettbewerbe in der JSON-Datei gefunden.")
else:
    for competition_url, comp_slug in competitions_json.items():
        print(f"Verarbeite Wettbewerb: {comp_slug}")

        # Pagination-Logik, um mehr als 20 Kernels zu kriegen
        all_kernels = []
        page = 1
        page_size = 100  # Maximal 100 Kernels pro Seite anfordern

        while True:
            try:
                kernels_page = api.kernels_list(
                    competition=comp_slug,
                    sort_by='dateCreated',
                    page=page,
                    page_size=page_size
                )
            except ApiException as e:
                # 404 bedeutet meistens: Wettbewerb ist unbekannt oder du hast keinen Zugriff
                if e.status == 404:
                    print(f"Fehler 404: Wettbewerb '{comp_slug}' nicht gefunden oder kein Zugriff.")
                    break
                else:
                    # Falls ein anderer Fehler auftritt, werfen wir ihn hoch
                    raise e

            # Wenn keine Kernels zurückkamen, sind wir am Ende
            if not kernels_page:
                break

            all_kernels.extend(kernels_page)

            # Wenn weniger als page_size Kernels zurückkamen, gibt es keine weiteren Seiten
            if len(kernels_page) < page_size:
                break
            page += 1

        # Wenn gar nichts gefunden oder Fehler auftrat:
        if not all_kernels:
            continue

        total_count = len(all_kernels)
        # Bis zu 50 Zufalls-Kernels aus allen auswählen
        sampled_kernels = random.sample(all_kernels, min(50, total_count))

        # Daten für Excel sammeln
        for kernel in sampled_kernels:
            excel_rows.append({
                "Competition URL": competition_url,
                "Competition Slug": comp_slug,
                "Total Notebooks": total_count,
                "Notebook Link": f"https://www.kaggle.com/{kernel.ref}"
            })

# Abschließend alle gesammelten Daten in ein Excel-Sheet schreiben
if excel_rows:
    df = pd.DataFrame(excel_rows)
    excel_path = os.path.join(output_dir, "competition_notebook_links.xlsx")
    df.to_excel(excel_path, index=False)
    print(f"\nExcel-Datei '{excel_path}' wurde gespeichert.")
else:
    print("Es wurden keine Kernel-Daten gefunden oder gespeichert.")
