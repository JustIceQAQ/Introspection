from abc import ABC, abstractmethod

from code.python_oop_and_solid.models import Article


class ArticleFilter(ABC):

    @abstractmethod
    def validate(self, article: Article) -> bool:
        raise NotImplementedError


class DefaultArticleFilter(ArticleFilter):
    def validate(self, article: Article) -> bool:
        return True


class GithubArticleFilter(ArticleFilter):
    def validate(self, article: Article) -> bool:
        return 'github.com' in article.site
