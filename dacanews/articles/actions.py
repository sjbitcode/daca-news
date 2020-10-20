import datetime
import pytz

from .clients import ClientFactory
from .models import Article, Source
from .forms import ApiResponseForm, ArticleForm, SourceForm


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


if __name__ == '__main__':
    factory = ClientFactory()
    news_api_client = factory.get_client('NewsApi')
    bing_client = factory.get_client('Bing')

    news_api_pipeline = ArticlePipeline(news_api_client)
    bing_pipeline = ArticlePipeline(bing_client)
