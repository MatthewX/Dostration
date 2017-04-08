from scrapy import Spider
from DoslationSpider.items import DoslationspiderItem
from scrapy import Request
import time
import urllib.request


class DoslationSpider(Spider):

    name = "doslationspider"
    allow_domains = ["http://english.actionemploirefugies.com/offers/Armee+De+Terre"]
    start_urls = ["http://english.actionemploirefugies.com/offers/Armee+De+Terre"]
    count = 0
    path = {
        "list": "//*[@class='results-classic']/div[@class='offer']/div[@class='candidate-button']/a[@class='c_button c_button inverse']",
        "position_name": ".//div[@class='job_ad']/h1/text()",
        "company": ".//div[@class='ad_info']/ul/li[3]/h2/text()",
        "type": ".//div[@class='ad_info']/ul/li[4]/h3/text()",
        "salary": ".//div[@class='ad_info']/ul/li[5]/span/text()",
        "location": ".//div[@class='ad_info']/ul/li[6]/span/text()",
        "description": ".//div[@class='jit_block_description']",
        "next_page": "//*[@id='pagination']/a[1]/@href",
        "prefix_url": "http://english.actionemploirefugies.com"
    }

    def parse(self, response):
        link_list = response.xpath(DoslationSpider.path["list"])
        for link in link_list:
            print("awesome")
            anchor = link.xpath("@href").extract()[0]
            content = str(urllib.request.urlopen(anchor).read())
            start_index = content.find("data-redirect-url=") + len('data-redirect-url="')
            end_index = content.find('"', start_index)
            final_url = content[start_index: end_index]
            yield Request(final_url, callback=self.parse_content)

        next_page = response.xpath(DoslationSpider.path["next_page"])
        if next_page and DoslationSpider.count < 5:
            print("test test")
            anchor = DoslationSpider.path["prefix_url"] + next_page.extract()[0]
            print(anchor)
            content = str(urllib.request.urlopen(anchor).read())
            start_index = content.find("data-redirect-url=") + len('data-redirect-url="')
            end_index = content.find('"', start_index)
            final_url = content[start_index: end_index]
            DoslationSpider.count += 1
            yield Request(final_url, callback=self.parse_content)

    def parse_content(self, response):
        item = DoslationspiderItem()
        # item['link'] = response.url
        item['position_name'] = response.xpath(DoslationSpider.path["position_name"]).extract()
        # item['company'] = response.xpath(DoslationSpider.path["company"]).extract()
        # item['type'] = response.xpath(DoslationSpider.path["type"]).extract()
        # item['salary'] = response.xpath(DoslationSpider.path["salary"]).extract()
        # item['location'] = response.xpath(DoslationSpider.path["location"]).extract()
        # item['description'] = response.xpath(DoslationSpider.path["description"]).extract()
        return item
