from abc import ABCMeta, abstractmethod
import datetime
import os
import pytz
import requests

from .models import Article, Source
from .forms import ApiResponseForm, ArticleForm, SourceForm


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


factory = ClientFactory()

###########################################################

bing = factory.get_client('Bing')
news_api = factory.get_client('NewsApi')


class ArticlePipeline:
    def __init__(self, news_client, params={}):
        self.news_client = news_client
        self.params = params

    @staticmethod
    def check_duplicate_article_diff_source_exist(article_dict):
        """
        Check if an article with the same title exist between
        the current date and 15 days back, since an article
        can have the same name but from a different source.
        """
        title = article_dict.get('title')
        end_date = datetime.datetime.today().replace(tzinfo=pytz.UTC)
        start_date = end_date - datetime.timedelta(days=15)

        return Article.objects.filter(title=title).filter(
            published_at__range=(start_date, end_date)).exists()

    @staticmethod
    def is_new_article(article_dict):
        """
        Validate whether an article should be saved by checking
        some edge cases.
        Do not save (return False) if any edge case function returns True.
        """
        return not any([
            ArticlePipeline.check_duplicate_article_diff_source_exist(article_dict)
        ])

    @staticmethod
    def get_source(source_dict):
        """
        Get or create a Source instance from news_client response.
        """
        # Check if source exists in db first.
        # Use only name because form validation populates slug if empty.
        source = Source.objects.filter(name=source_dict.get('name')).first()
        if source:
            return source

        # If source is new, populate and attempt to create from form.
        source_form = SourceForm(source_dict)
        if not source_form.is_valid():
            # Insert logging here
            print(source_form.errors)
            return

        return source_form.save()

    @staticmethod
    def create_article(article_dict, source_obj):
        """
        Create Article instance from news_client response and source.
        """
        # Add source to news_client dict before populating form.
        article_dict['source'] = source_obj.id

        article_form = ArticleForm(article_dict)

        if not article_form.is_valid():
            # Insert logging here
            print(article_form.errors)
            return

        article_form.save()

    @staticmethod
    def create_api_response(api_resp_dict):
        """
        Create Api Response instance from news_client response.
        """
        api_resp_form = ApiResponseForm(api_resp_dict)

        if not api_resp_form.is_valid():
            # Insert logging here
            print(api_resp_form.errors)
            return

        api_resp_form.save()

    def fetch_and_save_articles(self):
        """
        Make news_client API call via instance fetch method, then
        validate and store articles, sources, and api response.
        """
        # Save articles and sources if valid.
        for article_dict, source_dict in self.news_client.fetch_articles(params=self.params):

            if ArticlePipeline.is_new_article(article_dict):
                source = ArticlePipeline.get_source(source_dict)
                if source:
                    ArticlePipeline.create_article(article_dict, source)

        # Save the API Response.
        ArticlePipeline.create_api_response({
            'source': str(self.news_client),
            'response': self.news_client.response.json(),
            'url': self.news_client.response.url
        })
