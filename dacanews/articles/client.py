from abc import ABCMeta, abstractmethod
import datetime
import html
import os
import pytz
import requests

from django.utils.html import strip_tags
from newsapi import NewsApiClient


class BaseClient(metaclass=ABCMeta):
    @abstractmethod
    def _fetch_articles(self, params={}):
        pass

    @abstractmethod
    def fetch_articles(self):
        pass

    @staticmethod
    def strip_tags_and_format(html_str):
        html_str = html.unescape(html_str)
        return strip_tags(html_str)


class NewsAPIClient(BaseClient):
    def __init__(self):
        self.api_key = os.path.join(
            os.environ.get('NEWSAPI_KEY'))
        self.client = NewsApiClient(api_key=self.api_key)
        self.base_url = 'https://newsapi.org/v2/everything'
        self.source_ids = [
            'abc-news', 'associated-press', 'cnn', 'fox-news', 'google-news', 'national-review',
            'nbc-news', 'newsweek', 'new-york-magazine', 'politico', 'the-american-conservative',
            'the-hill', 'the-huffington-post', 'the-wall-street-journal', 'the-washington-post',
            'the-washington-times', 'time', 'usa-today', 'wired'
        ]
        self.params = {
            'qintitle': 'daca',
            'language': 'en',
            'sort_by': 'relevancy',
            'from_param': (datetime.date.today() -
                           datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
            'to': datetime.date.today().strftime('%Y-%m-%d')
        }
        self.url = None
        self.response = None

    def _fetch_articles(self, params={}):
        p = {
            'qintitle': params.get('qintitle') or self.params.get('qintitle'),
            'language': params.get('language') or self.params.get('language'),
            'sort_by': params.get('sort_by') or self.params.get('sort_by'),
            'from_param': params.get('from_param') or self.params.get('from_param'),
            'to': params.get('to') or self.params.get('to')
        }
        self.response = self.client.get_everything(**p)

        # not used, but generated for storing purposes
        self.base_url = requests.Request('GET', self.base_url, params=p).prepare().url

    def fetch_articles(self, params={}):
        # response = self._fetch_articles(params=params)
        self._fetch_articles(params=params)

        for raw_article in self.response['articles']:
            article = {
                'author': raw_article.get('author', ''),
                'title': raw_article.get('title', ''),
                'description': raw_article.get('description', ''),
                'url': raw_article.get('url'),
                'image_url': raw_article.get('urlToImage', ''),
                'published_at': datetime.datetime.strptime(
                    raw_article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'
                ).replace(tzinfo=pytz.utc)
            }

            source = {
                'name': raw_article.get('source', {}).get('name'),
                'slug': raw_article.get('source', {}).get('id')
            }

            yield article, source


class BingClient(BaseClient):
    def __init__(self):
        self.api_key = os.environ.get('BING_SUBSCRIPTION_KEY')
        self.base_url = os.path.join(
            os.environ.get('BING_PROJECT_ENDPOINT'),
            'bing/v7.0/news/search'
        )
        self.headers = {'Ocp-Apim-Subscription-Key': self.api_key}
        self.params = {
            'q': 'daca',
            'textFormat': 'HTML',
            'mkt': 'en-US',
            'count': 10,
            'offset': 0,
            'sortBy': 'Date'
        }
        self.url = None
        self.response = None

    def _fetch_articles(self, params={}):
        p = {
            'q': params.get('q') or self.params.get('q'),
            'textFormat': params.get('textFormat') or self.params.get('textFormat'),
            'mkt': params.get('mkt') or self.params.get('mkt'),
            'count': params.get('count') or self.params.get('count'),
            'offset': params.get('offset') or self.params.get('offset'),
            'sortBy': params.get('sortBy') or self.params.get('sortBy'),
        }
        response = requests.get(self.base_url, headers=self.headers, params=p)
        self.url = response.request.url
        self.response = response.json()

    def fetch_articles(self, params={}):
        # response = self._fetch_articles(params=params)
        self._fetch_articles(params=params)

        for raw_article in self.response['value']:
            article = {
                'title': raw_article.get('name', ''),
                'description': raw_article.get('description', ''),
                'url': raw_article.get('url', ''),
                'image_url': raw_article.get('image', {}).get('thumbnail', {}).get('contentUrl', ''),
                'published_at': datetime.datetime.strptime(
                    raw_article.get('datePublished'),
                    '%Y-%m-%dT%H:%M:%S.0000000Z'
                ).replace(tzinfo=pytz.utc)
            }

            source = {
                'name': raw_article.get('provider', {})[0].get('name', ''),
                'slug': ''
            }

            yield article, source

    # def collect_sources(self):
    #     if not self.response:
    #         raise AttributeError('Response is None. _fetch_articles method must be called.')

    #     for article in self.response['value']:
    #         yield {
    #             'name': article['provider']['name'],
    #             'slug': ''
    #         }
