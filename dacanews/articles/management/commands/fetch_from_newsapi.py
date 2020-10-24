from django.core.management.base import BaseCommand

from articles.actions import news_api_pipeline
from articles.clients import NewsApiClient


# def paginate_newsapi(params):
#     page_size = params.get('page_size', 10)
#     page = params.get('page', 1)
#     offset = page_size * page
#     earliest_date = params.pop('earliest_date')

#     n = NewsApiClient()

#     """
#     What does paginate mean?
#     There is a defined number of results, and we got a subset.
#     We want all.
#     We have to get them in chunks until we get all.
#     """
#     total_results = 0  # n.response.json()['totalResults']
#     articles_fetched = 0  # len(n.response.json()['articles'])

#     while (page_size * page) + articles_fetched < total_results:
#         n._fetch_articles(params=params)
#         articles_fetched += len(n.response.json()['articles'])


class Command(BaseCommand):
    help = 'Fetch articles from NewsAPI'

    def handle(self, *args, **options):
        news_api_pipeline.fetch_and_save_articles()
