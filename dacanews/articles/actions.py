import datetime
import logging

import requests

from .clients import ClientFactory
from .exceptions import DacaNewsException
from .forms import ApiResponseForm, ArticleForm, SourceForm, strip_tags_and_format
from .models import Article, Source

logger = logging.getLogger(__name__)


class ArticlePipeline:
    def __init__(self, news_client):
        self.news_client = news_client

    @staticmethod
    def check_duplicate_article_diff_source_exist(article_dict):
        """
        Check if an article with the same title exist between
        the publish date and 15 days back, since an article
        can have the same name but from a different source.
        """
        title = strip_tags_and_format(article_dict.get('title'))
        end_date = article_dict['published_at'] + datetime.timedelta(days=15)
        start_date = article_dict['published_at'] - datetime.timedelta(days=15)
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
        name = strip_tags_and_format(source_dict.get('name'))
        source = Source.objects.filter(name__iexact=name).first()
        if source:
            return source

        # If source is new, populate and attempt to create from form.
        source_form = SourceForm(source_dict)
        if not source_form.is_valid():
            logger.error(source_form.errors.as_data(), extra={
                'source_name': source_dict.get('name'),
                'source_slug': source_dict.get('slug')
            })
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
            logger.error(article_form.errors.as_data(), extra={
                'article_title': article_dict.get('title'),
                'article_url': article_dict.get('url'),
                'article_author': article_dict.get('author'),
                'article_pub_date': article_dict.get('published_at')
            })
            return

        article_form.save()

    @staticmethod
    def create_api_response(api_resp_dict):
        """
        Create Api Response instance from news_client response.
        """
        api_resp_form = ApiResponseForm(api_resp_dict)

        if not api_resp_form.is_valid():
            logger.error(api_resp_form.errors.as_data())
            return

        api_resp_form.save()

    def fetch_and_save_articles(self, params={}):
        """
        Make news_client API call via instance fetch method, then
        validate and store articles, sources, and api response.
        """
        try:
            # Save articles and sources if valid.
            for article_dict, source_dict in self.news_client.fetch_articles(params=params):

                is_new = ArticlePipeline.is_new_article(article_dict)
                logger.debug(f'New Article Check --> {is_new}')

                if is_new:
                    source = ArticlePipeline.get_source(source_dict)
                    if source:
                        ArticlePipeline.create_article(article_dict, source)

            # Save the API Response.
            ArticlePipeline.create_api_response({
                'source': str(self.news_client),
                'response': self.news_client.response.json(),
                'url': self.news_client.response.url
            })

        except requests.exceptions.RequestException as e:
            raise DacaNewsException(
                f'{str(self.news_client)} has an issue fetching articles - '
                f'{str(e)}'
            )

        except Exception as e:
            raise DacaNewsException(
                f'Article pipeline issue with {str(self.news_client)} - '
                f'{str(e)}'
            )


factory = ClientFactory()
news_api_client = factory.get_client('NewsApi')
bing_client = factory.get_client('Bing')

newsapi_default_params = {
    'qintitle': 'daca',
    'language': 'en',
    'sortBy': 'publishedAt',
    'pageSize': 100,
    'page': 1,
    'from_param': (datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d'),
    'to': datetime.date.today().strftime('%Y-%m-%d')
}

bing_default_params = {
    'q': 'daca',
    'textFormat': 'HTML',
    'mkt': 'en-US',
    'count': 100,
    'offset': 0,
    'sortBy': 'Date',
    'max_pages': 1  # Internal param for pagination
}

news_api_pipeline = ArticlePipeline(news_api_client)
bing_pipeline = ArticlePipeline(bing_client)
