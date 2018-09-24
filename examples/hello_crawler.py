from collections import defaultdict

import aiofiles # external dependency
import lxml.html as lh
from scrapio.scrapers.base_scraper import BaseScraper
from scrapio.utils.helpers import response_to_html


class OurScraper(BaseScraper):

    def parse_result(self, response):
        html = response_to_html(response)
        dom = lh.fromstring(html)

        result = defaultdict(lambda: "N/A")
        result['url'] = response.url
        title = dom.cssselect('title')
        h1 = dom.cssselect('h1')
        if title:
            result['title'] = title[0].text_content()
        if h1:
            result['h1'] = h1[0].text_content()
        return result

    async def save_results(self, result):
        if result:
            async with aiofiles.open('example_output.csv', 'a') as f:
                url = result.get('url')
                title = result.get('title')
                h1 = result.get('h1')
                await f.write('"{}","{}","{}"\n'.format(url, title, h1))


if __name__ == '__main__':
    scraper = OurScraper.create_scraper('http://edmundmartin.com')
    scraper.run_scraper(10, 2)