# MA_WEM - Labo 1

Auteurs : Cardoso Rafael, Maksimous Thomas et Manzini Kylian

## 2.1 : Éléments scrappé

Nous avons choisi des articles sur Wikipédia.org. Les données scrappées sont le titre de la page web et les headings H1 à H4 de l'article.

Il est possible de récupérer le contenu des headings et du titre en utilisant les selecteurs scrapy. Voici un extrait de code :

~~~python
    headings = response.css(".mw-heading")
    heading.css("h2::text").get()
    heading.css("h3::text").get()
    heading.css("h4::text").get()
~~~

## 2.3 : Recherche

### Explication de la syntaxe

Dans ElasticSearch, une recherche simple peut être effectuée grâce à l'API _search.  
La requête peut être formulée sous forme structurée grâce à Query DSL, qui est le format JSON utilisé pour décrire précisément la recherche à effectuer.
Ce langage permet notamment de définir le type de requête à utiliser, comme match ou multi_match. Dans notre cas, le choix s’est porté sur multi_match, car cette requête permet d’effectuer une recherche simultanément dans plusieurs champs de l’index.

### Recherche dans des champs spécifiques
Pour limiter la recherche à certains champs uniquement, Elasticsearch permet de préciser ces derniers dans le paramètre fields. Il est ainsi possible de restreindre la recherche aux champs jugés pertinents, au lieu d’interroger l’ensemble du contenu indexé. Dans notre implémentation, cette approche a permis de cibler les champs title, headings_h2, headings_h3 et headings_h4.

### Boosting
Elasticsearch permet d’accorder plus d’importance à certains champs grâce au mécanisme de boosting. Celui-ci s’exprime directement dans le paramètre fields avec la syntaxe champ^n, où n représente un facteur de pondération. Dans notre implémentation, on a boosté le champ title : title^2, ce que signifie qu’une correspondance trouvée dans le champ title aura davantage de poids dans le calcul du score de pertinence qu’une correspondance trouvée dans un champ non boosté.

Références 
- https://www.elastic.co/docs/reference/query-languages/querydsl

## 2.4.2 Fuzzy Query

La recherche floue (fuzzy query) dans Elasticsearch permet de retrouver des documents contenant des termes proches du terme recherché, même lorsqu’il existe de légères différences orthographiques. Elle repose sur la distance d’édition de Levenshtein, c’est-à-dire le nombre minimal de modifications nécessaires pour transformer un mot en un autre : ajout, suppression, remplacement ou inversion de caractères. Dans notre cas, nous avons testé ce mécanisme dans le fichier fuzzysearch.py.

Cependant, cette approche est surtout adaptée à de petites fautes de frappe ou à des variations limitées. En pratique, la recherche floue d’Elasticsearch fonctionne avec une tolérance faible, par exemple 0, 1, 2 ou AUTO. Cela signifie qu’elle convient bien pour des erreurs mineures, mais qu’elle n’est pas forcément optimale pour couvrir un grand nombre de variantes orthographiques d’un prénom tout en conservant de bonnes performances.

Dans le cas de prénoms comme Caitlin, qui peuvent avoir de nombreuses variantes, une meilleure alternative serait d’utiliser le plugin phonetic analysis. Celui-ci transforme les mots en représentation phonétique à l’aide d’algorithmes comme Soundex ou Metaphone, ce qui permet de rapprocher des formes différentes mais prononcées de manière similaire. Cette approche est donc plus adaptée lorsque les variations ne sont pas seulement des fautes de frappe, mais de vraies variantes orthographiques.

Références
- https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-fuzzy-query
- https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-phonetic
