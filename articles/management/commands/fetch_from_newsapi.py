from django.core.management.base import BaseCommand

from articles.actions import news_api_pipeline, newsapi_default_params


class Command(BaseCommand):
    help = 'Fetch articles from NewsAPI'

    def handle(self, *args, **options):
        news_api_pipeline.fetch_and_save_articles(params=newsapi_default_params)
