from pathlib import Path
import json

from elasticsearch_dsl import Document, Text, Keyword, connections


class WikipediaDocument(Document):
    """
    Modèle Elasticsearch pour les documents Wikipédia indexés
    à partir du fichier wikipedia.ndjson produit en partie 1.
    """

    url = Keyword()
    title = Text()
    # On indexe les clés (titres) de l'arborescence comme texte concaténé
    headings_h2 = Text()
    headings_h3 = Text()
    headings_h4 = Text()

    class Index:
        name = "wikipedia"


def _extract_headings_levels(headings: dict):
    """
    À partir de la structure hiérarchique des titres,
    fabrique trois listes à plat: h2, h3, h4.
    """
    h2_list = []
    h3_list = []
    h4_list = []

    if not isinstance(headings, dict):
        return h2_list, h3_list, h4_list

    for h2, sub_h3 in headings.items():
        h2_list.append(h2)
        if isinstance(sub_h3, dict):
            for h3, sub_h4 in sub_h3.items():
                h3_list.append(h3)
                if isinstance(sub_h4, dict):
                    for h4 in sub_h4.keys():
                        h4_list.append(h4)

    return h2_list, h3_list, h4_list


def index_wikipedia_ndjson(
    ndjson_path: str = "wikipedia.ndjson",
    es_hosts=None,
    index_name: str = "wikipedia",
):
    """
    Lit le fichier wikipedia.ndjson produit par le crawler (partie 1)
    et indexe chaque ligne dans Elasticsearch avec elasticsearch-dsl.
    """
    if es_hosts is None:
        es_hosts = ["http://localhost:9200"]

    path = Path(ndjson_path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier NDJSON introuvable: {path}")

    # Connexion à Elasticsearch
    connections.create_connection(hosts=es_hosts)

    # Configurer le nom de l'index
    WikipediaDocument.Index.name = index_name

    # Créer l'index + mapping si nécessaire
    WikipediaDocument.init()

    # Lire chaque ligne du fichier NDJSON et indexer
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)
            url = data.get("url")
            title = data.get("title")
            headings = data.get("headings", {})

            h2_list, h3_list, h4_list = _extract_headings_levels(headings)

            doc = WikipediaDocument(
                url=url,
                title=title,
                headings_h2="; ".join(h2_list),
                headings_h3="; ".join(h3_list),
                headings_h4="; ".join(h4_list),
            )
            doc.save()

    print(f"Indexation terminée dans l'index '{index_name}'.")


if __name__ == "__main__":
    # Utilisation par défaut:
    # - lit scrappy/wikipedia.ndjson (lancer depuis le dossier scrappy)
    # - index 'wikipedia' sur http://localhost:9200
    index_wikipedia_ndjson()

