from abc import ABCMeta, abstractmethod
import datetime
import logging
import math
import os
import pdb
import pytz
import time
from urllib import parse

import requests

from .exceptions import DacaNewsException

logger = logging.getLogger(__name__)


class BaseClient(metaclass=ABCMeta):
    def __init__(self):
        self.base_url = None
        self.api_key = None
        # self.headers = {}
        self.response: requests.Response = None
        self.datetime_format_str = None

    @property
    def response_url(self):
        if not self.response:
            raise Exception('No response stored')
        return self.response.url

    def get_datetime(self, datetime_str):
        return datetime.datetime.strptime(
            datetime_str, self.datetime_format_str
        ).replace(tzinfo=pytz.utc)

    def get_date(self, datetime_str):
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

    @abstractmethod
    def _fetch_articles(self, params={}):
        """
        This method should make a request to an API's endpoint
        (using the requests library) to fetch articles and
        store the requests Response object as self.response.
        """
        pass

    @abstractmethod
    def fetch_articles(self):
        """
        This method should return an iterable of prepared article
        and source dicts.
        Article and source dict keys should match the ArticleForm
        and SourceForm fields.
        """
        pass


class NewsApiClient(BaseClient):
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

    def _fetch_articles(self, params={}):
        """
        Makes an API call to the 'everything' NewsAPI endpoint with
        given or default params and stores the request Response object
        to self.response.

        https://newsapi.org/docs/endpoints/everything
        """
        everything_endpoint = os.path.join(self.base_url, 'everything')
        p = {
            'qintitle': params.get('qintitle') or 'daca',
            'language': params.get('language') or 'en',
            'sortBy': params.get('sortBy') or 'publishedAt',
            'pageSize': params.get('pageSize') or 100,
            'page': params.get('page') or 1,
            'from_param': params.get('from_param') or
            (datetime.date.today() - datetime.timedelta(days=2)
             ).strftime('%Y-%m-%d'),
            'to': params.get('to') or datetime.date.today().strftime('%Y-%m-%d')
        }
        self.response = requests.get(everything_endpoint, headers=self.headers,
                                     params=p)
        # https://github.com/psf/requests/blob/143150233162d609330941ec2aacde5ed4caa510/requests/models.py#L920
        self.response.raise_for_status()

    def fetch_articles(self, params={}):
        """
        Yield article and source dicts from each article in self.response.
        """
        self._fetch_articles(params=params)  # populates self.response

        logger.info(f"Fetched {len(self.response.json()['articles'])} articles")

        for raw_article in self.response.json()['articles']:
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

    def _fetch_articles(self, params={}):
        """
        Makes an API call to the news search Bing endpoint with
        given or default params and stores the request Response object
        to self.response.

        https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-news-api-v7-reference
        """
        news_search_endpoint = os.path.join(self.base_url, 'news/search')
        p = {
            'q': params.get('q') or 'daca',
            'textFormat': params.get('textFormat') or 'HTML',
            'mkt': params.get('mkt') or 'en-US',
            'count': params.get('count') or 10,
            'offset': params.get('offset') or 0,
            'sortBy': params.get('sortBy') or 'Date',
        }
        self.response = requests.get(news_search_endpoint, headers=self.headers, params=p)
        # https://github.com/psf/requests/blob/143150233162d609330941ec2aacde5ed4caa510/requests/models.py#L920
        self.response.raise_for_status()

    def fetch_articles(self, params={}):
        """
        Yield article and source dicts from each article in self.response.
        """
        self._fetch_articles(params=params)  # populates self.response

        logger.info(f"Fetched {len(self.response.json()['value'])} articles")

        for raw_article in self.response.json()['value']:
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


class BasePaginator(metaclass=ABCMeta):

    def get_url_query_param(self, url, value):
        url_parts = parse.parse_qs(parse.urlparse(url).query)
        return url_parts.get(value)[0]

    @abstractmethod
    def page_size(self):
        pass

    @abstractmethod
    def total_results(self):
        pass

    @property
    def total_pages(self):
        return math.ceil(self.total_results / self.page_size)

    @abstractmethod
    def current_page(self):
        pass

    @abstractmethod
    def _get_next_params(self):
        pass

    def continue_pagination(self):
        print(
            f'current page {self.current_page}, {type(self.current_page)}, {self.total_pages}, {type(self.total_pages)}')
        return self.current_page < self.total_pages

    def get_next_params(self):
        if not self.continue_pagination():
            raise DacaNewsException('Cannot paginate further')
        return self._get_next_params()


class BingPaginatorMixin(BasePaginator):
    @property
    def offset(self):
        return int(self.get_url_query_param(self.response_url, 'offset'))

    @property
    def page_size(self):
        return int(self.get_url_query_param(self.response_url, 'count'))

    @property
    def total_results(self):
        return self.response.json()['totalEstimatedMatches']

    @property
    def current_page(self):
        # what page are we currently on
        # offset is 0 based, so we add 1 to mean page 1 was initial
        return self.offset // self.page_size + 1

    def _get_next_params(self):
        return {'offset': self.offset + self.page_size}

    def paginate(self, params={}):
        """
        This functionality will have to go in ArticlePipeline class, since it needs to
        wrap the iterating/saving of articles.
        """
        # Make initial request
        self._fetch_articles()

        # print(f'TOTAL RESULTS -- {self.total_results}')
        # print(f'TOTAL PAGES -- {self.total_pages}')
        # print(f'PAGE SIZE -- {self.page_size}')
        # print(f'CURRENT PAGE -- {self.current_page}')
        counter = 0
        while self.continue_pagination():
            if counter >= 3:
                print('circuit breaker!!!!!!!!!!!!!!!!!')
                break
            print(f'TOTAL RESULTS -- {self.total_results}')
            print(f'TOTAL PAGES -- {self.total_pages}')
            print(f'PAGE SIZE -- {self.page_size}')
            print(f'CURRENT PAGE -- {self.current_page}')
            print(f'NEXT PARAMS -- {self.get_next_params()}')
            # import pdb
            pdb.set_trace()
            self._fetch_articles(params={**params, **self.get_next_params()})
            counter += 1
            time.sleep(2)


class NewsApiPaginatorMixin(BasePaginator):
    @property
    def page_size(self):
        return int(self.get_url_query_param(self.response_url, 'pageSize'))

    @property
    def total_results(self):
        return self.response.json()['totalResults']

    @property
    def current_page(self):
        return int(self.get_url_query_param(self.response_url, 'page'))

    def _get_next_params(self):
        return {'page': self.current_page + 1}


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
