from collections import defaultdict
from lxml import html as lh

from scrapio.mixins.mongo import MongoMixin
from scrapio.crawlers import BaseCrawler


class OurMongoScraper(MongoMixin, BaseCrawler):

    def parse_result(self, html, response):
        dom = lh.fromstring(html)

        result = defaultdict(lambda: "N/A")
        result['url'] = str(response.url)
        title = dom.cssselect('title')
        h1 = dom.cssselect('h1')
        if title:
            result['title'] = title[0].text_content()
        if h1:
            result['h1'] = h1[0].text_content()
        return dict(result)


if __name__ == '__main__':
    crawler = OurMongoScraper('http://edmundmartin.com')
    crawler.create_mongo_client('mongodb://localhost:27017/', 'example', 'crawl')
    crawler.run_scraper(10)