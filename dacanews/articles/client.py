from abc import ABCMeta, abstractmethod
import datetime
import os
import pytz
import requests


class BaseClient(metaclass=ABCMeta):
    def __init__(self):
        self.base_url = None
        self.api_key = None
        self.headers = {}
        self.response: requests.Response = None

    @property
    def response_url(self):
        if not self.response:
            raise Exception('No response stored')
        return self.response.url

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
        self.headers['X-Api-Key'] = self.api_key

    def __str__(self):
        return 'NewsAPI'

    def __repr__(self):
        return 'NewsApiClient()'

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
            'sort_by': params.get('sort_by') or 'relevancy',
            'from_param': params.get('from_param') or
            (datetime.date.today() - datetime.timedelta(days=2)
             ).strftime('%Y-%m-%d'),
            'to': params.get('to') or datetime.date.today().strftime('%Y-%m-%d')
        }
        self.response = requests.get(everything_endpoint, headers=self.headers,
                                     params=p)

    def fetch_articles(self, params={}):
        """
        Yield article and source dicts from each article in self.response.
        """
        self._fetch_articles(params=params)  # populates self.response

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
        self.headers['Ocp-Apim-Subscription-Key'] = self.api_key

    def __str__(self):
        return 'Bing'

    def __repr__(self):
        return 'BingClient()'

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
            'count': params.get('count') or 3,
            'offset': params.get('offset') or 0,
            'sortBy': params.get('sortBy') or 'Date',
        }
        self.response = requests.get(news_search_endpoint, headers=self.headers, params=p)

    def fetch_articles(self, params={}):
        """
        Yield article and source dicts from each article in self.response.
        """
        self._fetch_articles(params=params)  # populates self.response

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
