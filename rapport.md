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
