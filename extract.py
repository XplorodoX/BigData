import json
from kaggle.api.kaggle_api_extended import KaggleApi


def extrahiere_letzten_abschnitt(url):
    """
    Extrahiert den letzten Abschnitt des Pfads einer URL.

    Args:
        url (str): Die vollständige URL.

    Returns:
        str: Der letzte Abschnitt der URL.
    """
    return url.rstrip('/').split('/')[-1]


def kaggle_wettbewerbe_links(limit=20):
    """
    Ruft die Links der neuesten Kaggle-Wettbewerbe ab.

    Args:
        limit (int): Die Anzahl der Wettbewerbe, deren Links abgerufen werden sollen.

    Returns:
        list: Eine Liste von Wettbewerbs-URLs.
    """
    api = KaggleApi()
    try:
        api.authenticate()
        # Ohne page_size, mit group='general'
        wettbewerbe = api.competitions_list(sort_by='recentlyCreated', group='general')
        links = [f"https://www.kaggle.com/competitions/{wettbewerb.ref}" for wettbewerb in wettbewerbe[:limit]]
        return links
    except Exception as e:
        print(f"Fehler beim Abrufen der Kaggle-Wettbewerbe: {e}")
        return []


def urls_zu_json(urls, output_file, kompakt=False):
    """
    Verarbeitet eine Liste von URLs und speichert die letzten Abschnitte in einer JSON-Datei.

    Args:
        urls (list): Liste von URLs.
        output_file (str): Der Dateiname der JSON-Ausgabedatei.
        kompakt (bool): Ob die JSON-Ausgabe komprimiert sein soll (default: False).

    Returns:
        str: Erfolgsmeldung mit dem Dateipfad.
    """
    result = {url: extrahiere_letzten_abschnitt(url) for url in urls}
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=None if kompakt else 4)
        return f"Die Daten wurden erfolgreich in '{output_file}' gespeichert."
    except Exception as e:
        return f"Fehler beim Speichern der Datei '{output_file}': {e}"


# Hauptlogik
if __name__ == "__main__":
    limit = 20
    output_file = 'kaggle_wettbewerbe.json'

    # Abrufen der Kaggle-Wettbewerbs-Links
    urls = kaggle_wettbewerbe_links(limit)

    if urls:
        # JSON-Datei speichern
        message = urls_zu_json(urls, output_file)
        print(message)
    else:
        print("Keine Wettbewerbs-URLs verfügbar.")
