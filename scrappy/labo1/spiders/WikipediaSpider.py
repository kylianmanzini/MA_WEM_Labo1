from pathlib import Path

import scrapy
import json

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        "https://fr.wikipedia.org/wiki/Métro_de_Rennes",
        "https://en.wikipedia.org/wiki/World_War_II",
        "https://fr.wikipedia.org/wiki/Guerre_de_Canudos",
        "https://en.wikipedia.org/wiki/Special:Random"
    ]

    counter = 0
        
    def parse(self, response):
        self.counter = self.counter + 1
        filename = f"wikipedia-{self.counter}.json"
        
        headings = response.css(".mw-heading")

        result = dict()
        
        result["url"] = response.url
        result["title"] = response.css("title::text").get()
        result["headings"] = dict()

        for heading in headings:
            current = "<not set>"
            if heading.css(".mw-heading2") != []:
                current = heading.css("h2::text").get()
                result["headings"][current] = dict()
                last_h2 = current
            elif heading.css(".mw-heading3") != []:
                current = heading.css("h3::text").get()
                result["headings"][last_h2][current] = dict()
                last_h3 = current
            elif heading.css(".mw-heading4") != []:
                current = heading.css("h4::text").get()
                result["headings"][last_h2][last_h3][current] = dict()
            print(current)

        print(result)
        
        json_result = json.dumps(result, indent=4, ensure_ascii=False)
            
        Path(filename).write_text(json_result, "utf-8")
        
        
        self.log(f"Saved file {filename}")
