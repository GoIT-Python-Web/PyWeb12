import json
import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

base_url = "https://index.minfin.com.ua/ua/russian-invading/casualties"


def get_urls():
    urls = ["/"]
    html_doc = requests.get(base_url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')  # TODO replace lxlm
    content = soup.select("div[class=ajaxmonth] h4[class=normal] a")
    prefix = "/month.php?month="
    for link in content:
        urls.append(prefix + re.search(r"\d{4}-\d{2}", link["href"]).group())
    return urls


def spider(url):
    result = []
    html_doc = requests.get(base_url + url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    content = soup.select("ul[class=see-also] li[class=gold]")
    for el in content:
        parse_element = {}
        date_key = el.find('span', attrs={"class": "black"}).text
        try:
            date_key = datetime.strptime(date_key, "%d.%m.%Y").isoformat()
        except ValueError:
            logging.error(f"Error for date: {date_key}")
            continue
        parse_element.update({"date": date_key})
        losses = el.find('div').find('div').find('ul')
        for l in losses:
            name, quantity, *_ = l.text.split("—")
            name = name.strip()
            quantity = re.search(r"\d+", quantity).group()
            parse_element.update({name: quantity})
        result.append(parse_element)
    return result


def main(urls):
    data = []
    for url in urls:
        data.extend(spider(url))
    return data


if __name__ == '__main__':
    urls = get_urls()
    result = main(urls)
    # print(result)
    with open("ups.json", "w", encoding="utf-8") as fd:
        json.dump(result, fd, ensure_ascii=False)
