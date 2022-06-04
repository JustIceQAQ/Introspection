import dataclasses
import io
import sys
from typing import Iterable, List, TextIO, Optional

import requests
from bs4 import BeautifulSoup


@dataclasses.dataclass
class Article:
    title: str
    link: str
    site: str
    points: int
    comments: int


class ArticleWriter:
    def __init__(self, fp: TextIO, title: str):
        self.fp = fp
        self.title = title

    def write(self, articles: List[Article]):
        self.fp.write(f'# {self.title}\n\n')
        for i, article in enumerate(articles, 1):
            self.fp.write(f'> TOP {i}: {article.title}\n')
            self.fp.write(f'> site: {article.site}\n')
            self.fp.write(f'> points：{article.points} comments：{article.comments}\n')
            self.fp.write(f'> link：{article.link}\n')
            self.fp.write('------\n')


class HackerNewsCrawler:
    root_url = 'https://news.ycombinator.com/'
    filename = "Hacker_News"

    def __init__(self, limit: int = 5):
        self.limit = limit

    def fetch(self) -> Iterable[Article]:
        response = requests.get(self.root_url)
        formatted = BeautifulSoup(response.text, "html5lib")
        raw_item_list = formatted.select("table.itemlist > tbody > tr")
        item_list = self.clean_data(raw_item_list)
        for item in item_list[:self.limit]:
            # print(item)
            title_link = item.select_one("a.titlelink")
            title = title_link.get_text()
            link = title_link["href"]
            site = item.select_one("span.sitestr").get_text()
            points = item.select_one("span.score").get_text().split(" ")[0].strip()
            comments = item.select("a")[-1].get_text().split(" ")[0].strip()
            yield Article(title=title, link=link, site=site, points=int(points), comments=int(comments))

    def clean_data(self, raw_item_list):
        item_list = []
        item_temp = ""
        for raw_item in raw_item_list:
            if (raw_item_str := str(raw_item)) not in ['<tr class="spacer" style="height:5px"></tr>']:
                item_temp += raw_item_str
            else:
                item_list.append(BeautifulSoup(item_temp, "html5lib"))
                item_temp = ""
        return item_list


def show_the_hacker_news(fp: Optional[TextIO] = None):
    dest_fp = fp or sys.stdout
    hacker_news_crawler = HackerNewsCrawler()
    hacker_news_dataset = hacker_news_crawler.fetch()
    writer = ArticleWriter(dest_fp, hacker_news_crawler.filename)
    writer.write(list(hacker_news_dataset))


if __name__ == '__main__':
    show_the_hacker_news()
