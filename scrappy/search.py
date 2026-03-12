from elasticsearch import Elasticsearch

def search_program() :

    # Connexion au client Elastic
    client = Elasticsearch("http://localhost:9200")

    print("Que veux-tu chercher? :")

    recherche = input()

    # Query pour faire la recherche dans l'index
    # title^2 --> application d'un boost
    response = client.search(
        index="wikipedia",
        query={
            "multi_match": {
                "query": recherche,
                "fields": ["title^2", "headings_h2", "headings_h3", "headings_h4"]
            }
        },
        highlight={
            "fields": {
                "title": {},
                "headings_h2": {},
                "headings_h3": {},
                "headings_h4": {}
            }
        }
    )

    # Récupération des résultats
    hits = response["hits"]["hits"]

    # Affichage de champs particuliers
    for hit in hits:
        score = hit["_score"]
        source = hit["_source"]["title"]
        highlight = hit["highlight"]
        print(score, source, highlight)

if __name__ == "__main__":
    search_program()

