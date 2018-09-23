from typing import List
from urllib.parse import urlparse, urljoin

from aiohttp import ClientResponse
import lxml.html as lh

from scrapio.structures.filtering import AbstractURLFilter, URLFilter
from scrapio.parsing.valid_url import valid_url


def link_extractor(response: ClientResponse, url_filter: URLFilter, defrag: bool) -> List[str]:
    html = response._body.decode('utf-8', errors='ignore')
    req_url = response.url
    dom = lh.fromstring(html)
    found_urls = []
    for href in dom.xpath('//a/@href'):
        url = urljoin(str(req_url), href)
        netloc = urlparse(url).netloc
        can_crawl = url_filter.can_crawl(netloc, url)
        if can_crawl and valid_url(url):
            found_urls.append(url)
    return found_urls