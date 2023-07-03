import re

import scrapy


class GetUrlsSpider(scrapy.Spider):
    name = "get_urls"
    allowed_domains = ["index.minfin.com.ua"]
    start_urls = ["https://index.minfin.com.ua/ua/russian-invading/casualties"]

    def parse(self, response, **kwargs):
        prefix = "/month.php?month="
        # /html/body/main/div/div/div[1]/div/div[1]/article/div[3]
        # //*[@id="idx-content"]/div[3]
        content = response.xpath("//div[@class='ajaxmonth']/h4[@class='normal']/a")
        for link in content:
            yield {
                "link": prefix + re.search(r"\d{4}-\d{2}", link.xpath("@href").get()).group()
            }
