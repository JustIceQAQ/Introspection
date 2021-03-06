import dataclasses
import io
import sys
from collections import Counter
from itertools import chain
from typing import Iterable, List, TextIO, Optional

import requests
from bs4 import BeautifulSoup

from code.python_oop_and_solid.filter import ArticleFilter, DefaultArticleFilter, GithubArticleFilter
from code.python_oop_and_solid.models import Article


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
    root_url = 'https://news.ycombinator.com'
    filename = "Hacker_News"

    def __init__(self, limit: int = 5, page: int = 1, article_filter: Optional[ArticleFilter] = None):
        self.limit = limit
        self.page = page
        self.article_filter = article_filter or DefaultArticleFilter()

    def fetch(self) -> Iterable[Article]:

        item_list = list(chain.from_iterable([self.formatting(p) for p in range(1, self.page + 1)]))
        counter = 0
        for item in item_list:
            if counter >= self.limit:
                break
            title_link = item.select_one("a.titlelink")
            title = title_link.get_text()
            link = title_link["href"]
            site = (get_site.get_text()
                    if (get_site := item.select_one("span.sitestr"))
                    else "-")
            points = check_points if (check_points := (get_points.get_text().split(" ")[0].strip()
                                                       if (get_points := item.select_one("span.score"))
                                                       else "0")
                                      ).isnumeric() else 0

            comments = check_comments if (check_comments := (get_comments.get_text().split(" ")[0].strip()
                                                             if (get_comments := item.select("a")[-1])
                                                             else "0")
                                          ).isnumeric() else 0

            article = Article(title=title, link=link, site=site, points=int(points), comments=int(comments))

            if self.article_filter.validate(article):
                counter += 1
                yield article

    def formatting(self, p):
        response = requests.get(f"{self.root_url}/news?p={p}")
        formatted = BeautifulSoup(response.text, "html5lib")
        raw_item_list = formatted.select("table.itemlist > tbody > tr")
        item_list = self.clean_data(raw_item_list)
        return item_list

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


class HackerNewsSiteSourceGrouper:
    def __init__(self, url: str, page: int = 5):
        self.root_url = url
        self.page = page

    def get_groups(self):
        elems = list(chain.from_iterable([self.formatting(p) for p in range(1, self.page + 1)]))

        groups = Counter()
        for elem in elems:
            groups.update([elem.get_text()])
        return groups

    def formatting(self, p):
        response = requests.get(f"{self.root_url}/news?p={p}")
        formatted = BeautifulSoup(response.text, "html5lib")
        raw_item_list = formatted.select("span.sitestr")
        return raw_item_list


def show_the_hacker_news(fp: Optional[TextIO] = None):
    dest_fp = fp or sys.stdout
    hacker_news_crawler = HackerNewsCrawler(page=1, article_filter=GithubArticleFilter())
    hacker_news_dataset = hacker_news_crawler.fetch()
    writer = ArticleWriter(dest_fp, hacker_news_crawler.filename)
    writer.write(list(hacker_news_dataset))


if __name__ == '__main__':
    # show_the_hacker_news()
    hacker_news_site_source_grouper = HackerNewsSiteSourceGrouper('https://news.ycombinator.com', page=5).get_groups()
    for key, value in hacker_news_site_source_grouper.most_common(3):
        print(f'Site: {key} | Count: {value}')
