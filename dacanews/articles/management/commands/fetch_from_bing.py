import datetime
import logging
import time

from django.core.management.base import BaseCommand

# from articles.actions import bing_pipeline
from articles.actions import bing_client, ArticlePipeline


logger = logging.getLogger(__name__)


def backfill(count=100, offset=0):
    bing_pipeline = ArticlePipeline(bing_client)
    earliest_article_date = datetime.date.today()

    while earliest_article_date >= datetime.date(2017, 1, 1):

        logger.info('Sleeping for 2 seconds')
        time.sleep(5)

        print(f'COUNT - {count}')
        print(f'OFFSET - {offset}')
        bing_pipeline.fetch_and_save_articles(params={
            'count': count,
            'offset': offset
        })
        offset += 100

        print('TOTAL ESTIMATED RESULTS')
        print(f"{bing_pipeline.news_client.response.json()['totalEstimatedMatches']}\n")
        print('API FETCH URL')
        print(f'{bing_pipeline.news_client.response_url}\n')

        pub_date_str = bing_pipeline.news_client.response.json()['value'][-1]['datePublished']
        # earliest_article_date = datetime.datetime.strptime(
        #     pub_date_str, '%Y-%m-%dT%H:%M:%S.0000000Z').date()
        earliest_article_date = bing_client.get_date(pub_date_str)
        print(f'Updating Date to {earliest_article_date}\n\n')
        # import pdb
        # pdb.set_trace()


class Command(BaseCommand):
    help = 'Fetch articles from Bing'

    def handle(self, *args, **options):
        # bing_pipeline.fetch_and_save_articles()
        backfill()
