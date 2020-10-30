from abc import ABCMeta, abstractmethod
import datetime
import logging
import os
import pytz

import requests

from .exceptions import DacaNewsException
from .paginator import NewsApiPaginatorMixin, BingPaginatorMixin

logger = logging.getLogger(__name__)


class BaseClient(metaclass=ABCMeta):
    def __init__(self):
        self.base_url = None
        self.api_key = None
        self.response: requests.Response = None
        self.datetime_format_str = None

    @property
    def response_url(self):
        """
        The url that returned the response, derived
        from the requests Response object stored as
        self.response.
        """
        if not self.response:
            raise DacaNewsException('No response stored')
        return self.response.url

    def _get_datetime(self, datetime_str):
        """
        Helper function to return an aware datetime
        object based off the datetime format the API
        uses.
        """
        return datetime.datetime.strptime(
            datetime_str, self.datetime_format_str
        ).replace(tzinfo=pytz.utc)

    def _get_date(self, datetime_str):
        """
        Helper function to return a date object based
        off the datetime format the API uses.
        """
        return datetime.datetime.strptime(
            datetime_str, self.datetime_format_str
        ).replace(tzinfo=pytz.utc).date()

    @abstractmethod
    def headers(self):
        """
        This method should return a dictionary with any
        necessary header values needed. If not, just
        return an empty dict.
        """
        pass

    def make_request(self, url='', params={}):
        """
        This method makes a request to a given endpoint with supplied
        parameters and stored headers (using the requests library)
        to fetch articles and store the requests Response object as self.response.
        """
        logger.info(f'Fetching {url}')
        self.response = requests.get(url, headers=self.headers,
                                     params=params)
        # https://github.com/psf/requests/blob/143150233162d609330941ec2aacde5ed4caa510/requests/models.py#L920
        self.response.raise_for_status()

    @abstractmethod
    def _fetch_articles(self, params={}):
        """
        This method should make a request to an API's endpoint
        (using the requests library) to fetch articles and
        store the requests Response object as self.response.
        """
        pass

    @abstractmethod
    def _serialize_articles(self, article_iterable):
        """
        This method should yield an article and source dicts
        for each article from an article iterable returned by the API.

        The article and source dicts should match the fields of
        forms.ArticleForm and forms.SourceForm, respectively.
        """
        pass

    @abstractmethod
    def fetch_articles(self):
        """
        This method should call the _fetch_articles with any
        params needed.

        Here you can modify any params before passing to _fetch_articles.
        """
        pass


class NewsApiClient(BaseClient, NewsApiPaginatorMixin):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://newsapi.org/v2/'
        self.api_key = os.path.join(os.environ.get('NEWSAPI_KEY'))
        self.datetime_format_str = '%Y-%m-%dT%H:%M:%SZ'

    def __str__(self):
        return 'NewsAPI'

    def __repr__(self):
        return 'NewsApiClient()'

    @property
    def headers(self):
        return {'X-Api-Key': self.api_key}

    def _fetch_articles(self, params):
        """
        Makes an API call to the 'everything' NewsAPI endpoint with
        given params.

        https://newsapi.org/docs/endpoints/everything
        """
        everything_endpoint = os.path.join(self.base_url, 'everything')
        self.make_request(everything_endpoint, params)

    def _serialize_articles(self, article_list):
        """
        Yield article and source dicts from a NewsAPI article list.
        """
        for raw_article in article_list:
            article = {
                'author': raw_article.get('author', ''),
                'title': raw_article.get('title', ''),
                'description': raw_article.get('description', ''),
                'url': raw_article.get('url'),
                'image_url': raw_article.get('urlToImage', ''),
                'published_at': self._get_datetime(raw_article['publishedAt'])
            }

            source = {
                'name': raw_article.get('source', {}).get('name'),
                'slug': raw_article.get('source', {}).get('id')
            }

            yield article, source

    def fetch_articles(self, params={}):
        """
        Fetches articles via pagination.
        """
        max_pages = params.pop('max_pages', None)
        if max_pages == 0:
            raise DacaNewsException('Max pages has to be > 0')

        while True:
            self._fetch_articles(params=params)
            yield from self._serialize_articles(self.response.json()['articles'])
            if not self.continue_pagination(max_pages=max_pages):
                break
            params = {**params, **self.get_next_params()}


class BingClient(BaseClient, BingPaginatorMixin):
    def __init__(self):
        super().__init__()
        self.base_url = os.path.join(
            os.environ.get('BING_PROJECT_ENDPOINT'),
            'bing/v7.0/'
        )
        self.api_key = os.environ.get('BING_SUBSCRIPTION_KEY')
        self.datetime_format_str = '%Y-%m-%dT%H:%M:%S.0000000Z'

    def __str__(self):
        return 'Bing'

    def __repr__(self):
        return 'BingClient()'

    @property
    def headers(self):
        return {'Ocp-Apim-Subscription-Key': self.api_key}

    def _fetch_articles(self, params):
        """
        Makes an API call to the news search Bing endpoint with
        given params.

        https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-news-api-v7-reference
        """
        news_search_endpoint = os.path.join(self.base_url, 'news/search')
        self.make_request(url=news_search_endpoint, params=params)

    def _serialize_articles(self, article_list):
        """
        Yield article and source dicts from a Bing article list.
        """
        for raw_article in article_list:
            article = {
                'title': raw_article.get('name', ''),
                'description': raw_article.get('description', ''),
                'url': raw_article.get('url', ''),
                'image_url': raw_article.get('image', {}).get('thumbnail', {}).get('contentUrl', ''),
                'published_at': self._get_datetime(raw_article.get('datePublished'))
            }

            source = {
                'name': raw_article.get('provider', {})[0].get('name', ''),
                'slug': ''
            }

            yield article, source

    def fetch_articles(self, params={}):
        """
        Fetches articles via pagination.
        """
        max_pages = params.pop('max_pages', None)
        if max_pages == 0:
            raise DacaNewsException('Max pages has to be > 0')

        while True:
            self._fetch_articles(params=params)
            yield from self._serialize_articles(self.response.json()['value'])
            if not self.continue_pagination(max_pages=max_pages):
                break
            params = {**params, **self.get_next_params()}


class ClientFactory:

    @staticmethod
    def get_client(key):
        news_clients = {
            'NewsApi': NewsApiClient,
            'Bing': BingClient
        }
        client = news_clients.get(key)
        if not client:
            raise KeyError(key)
        return client()
