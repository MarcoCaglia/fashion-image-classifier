import hashlib

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest

from ..items import ZalandoItem


class ZalandoCrawlerSpider(CrawlSpider):
    name = 'zalando_crawler'
    allowed_domains = ['zalando.nl']
    start_urls = ['https://www.zalando.nl/dameskleding/']

    rules = (
        Rule(LinkExtractor(restrict_css="a.g88eG_.oHRBzn.LyRfpJ.JT3_zV.g88eG_.ONArL-._2dqvZS.lfPP-F"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css="a.cat_link-8qswi"), callback='parse_main', follow=True)
    )

    def start_requests(self):
        for url in ZalandoCrawlerSpider.start_urls:
            yield SplashRequest(url=url, callback=self.parse_main)

    def parse_main(self, response):
        pieces = ZalandoCrawlerSpider.rules[0].link_extractor \
            .extract_links(response)
        next_page = ZalandoCrawlerSpider.rules[1].link_extractor \
            .extract_links(response)
        next_page = next_page[-1] if len(next_page) > 1 else None

        for piece in pieces:
            yield SplashRequest(piece.url, callback=self.parse_piece)

        else:
            if next_page:
                yield SplashRequest(next_page.url, callback=self.parse_main)

    def parse_piece(self, response):
        item = ZalandoItem()
        item["url"] = response.url
        item["name"] = response.css('h1.OEhtt9.ka2E9k.uMhVZi.z-oVg8.pVrzNP.w5w9i_._1PY7tW._9YcI4f::text').extract_first()
        item["brand"] = response.css('h3.OEhtt9.ka2E9k.uMhVZi.uc9Eq5.pVrzNP._5Yd-hZ::text').extract_first()
        item["price"] = response.css('span.uqkIZw.ka2E9k.uMhVZi.FxZV-M.z-oVg8.pVrzNP::text').extract_first()
        if not item["price"]:
            item["price"] = response.css('span.uqkIZw.ka2E9k.uMhVZi.dgII7d.z-oVg8._88STHx.cMfkVL::text').extract_first()
        item["reviews"] = response.css("h5.ZcZXP0.ka2E9k.uMhVZi.z-oVg8.pVrzNP::text").extract_first()
        item["rating"] = response.css("span.AKpsL5.ka2E9k.uMhVZi.uc9Eq5.pVrzNP::text").extract_first()
        item["colour"] = response.css('span.u-6V88.ka2E9k.uMhVZi.dgII7d.z-oVg8.pVrzNP::text').extract_first()
        item["image"] = response.xpath('/html/body/div/div/div/div/div/x-wrapper-re-1-2/div/div') \
            .css('img._6uf91T.z-oVg8.u-6V88.ka2E9k.uMhVZi.FxZV-M._2Pvyxl.JT3_zV.EKabf7.mo6ZnF._1RurXL.mo6ZnF.PZ5eVw').xpath("@src").extract()
        item["item_id"] = hashlib.sha256(
            (str(item["name"]) + str(item["brand"]) + str(item["colour"]))
            .encode("utf-8")
            ).hexdigest()

        return item
