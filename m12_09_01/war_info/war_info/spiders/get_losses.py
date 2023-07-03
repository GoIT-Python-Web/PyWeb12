import json
import logging
import re
from datetime import datetime

import scrapy


def get_next_link():
    with open("links.json", "r", encoding='utf-8') as fd:
        result = json.load(fd)
    return [el.get("link") for el in result]


class GetLossesSpider(scrapy.Spider):
    name = "get_losses"
    allowed_domains = ["index.minfin.com.ua"]
    start_urls = ["https://index.minfin.com.ua/ua/russian-invading/casualties"]

    def parse(self, response, **kwargs):
        parse_element = {}
        content = response.css("ul[class=see-also] li[class=gold]")
        for el in content:
            date_key = el.xpath('span/text()').get()
            try:
                date_key = datetime.strptime(date_key, "%d.%m.%Y").isoformat()
            except ValueError:
                logging.error(f"Error for date: {date_key}")
                continue

            parse_element.update({"date": date_key})

            losses = el.xpath('div/div/ul/li')
            for l in losses:
                print(l.css('*::text').extract())
                name, quantity, *_ = ''.join(l.css('*::text').extract()).split("—")
                name = name.strip()
                quantity = re.search(r"\d+", quantity).group()
                parse_element.update({name: quantity})

            yield parse_element

        for next_link in get_next_link():
            yield scrapy.Request(self.start_urls[0] + next_link, method='GET')
