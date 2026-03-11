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

    output_file = "wikipedia.ndjson"

    def open_spider(self, spider):
        Path(self.output_file).write_text("", encoding="utf-8")

    def parse(self, response):
        headings = response.css(".mw-heading")

        data = {
            "url": response.url,
            "title": response.css("title::text").get(),
            "headings": {}
        }

        last_h2 = None
        last_h3 = None

        for heading in headings:
            h2 = heading.css("h2::text").get()
            h3 = heading.css("h3::text").get()
            h4 = heading.css("h4::text").get()

            if h2:
                data["headings"][h2] = {}
                last_h2 = h2
                last_h3 = None

            elif h3 and last_h2 is not None:
                data["headings"][last_h2][h3] = {}
                last_h3 = h3

            elif h4 and last_h2 is not None and last_h3 is not None:
                data["headings"][last_h2][last_h3][h4] = {}

        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

        self.log(f"Saved entry to {self.output_file}")