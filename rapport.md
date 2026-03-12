# MA_WEM Labo 1

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

