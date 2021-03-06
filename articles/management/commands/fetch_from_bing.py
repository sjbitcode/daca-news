
from django.core.management.base import BaseCommand

from articles.actions import bing_pipeline, bing_default_params


class Command(BaseCommand):
    help = 'Fetch articles from Bing'

    def handle(self, *args, **options):
        bing_pipeline.fetch_and_save_articles(params=bing_default_params)
