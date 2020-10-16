import datetime
import os
import pytz

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from newsapi import NewsApiClient

from articles.models import Article, Source


newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_KEY'))
source_ids = [
    'abc-news', 'associated-press', 'cnn', 'fox-news', 'google-news', 'national-review',
    'nbc-news', 'newsweek', 'new-york-magazine', 'politico', 'the-american-conservative',
    'the-hill', 'the-huffington-post', 'the-wall-street-journal', 'the-washington-post',
    'the-washington-times', 'time', 'usa-today', 'wired'
]


def fetch_and_store_articles():
    try:
        response = newsapi.get_everything(
            qintitle='daca',
            language='en',
            # sources=','.join(source_ids),
            sort_by='relevancy',
            # from_param='2020-09-15',
            from_param=(datetime.date.today() -
                        datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
            to=datetime.date.today().strftime('%Y-%m-%d')
        )

        print(f"Found {response['totalResults']} articles")

        with transaction.atomic():
            print('Get or create sources')

            unique_source_names = {
                # the id is sometimes none, but name always populated.
                article['source']['name']: {
                    'slug': article['source'].get('id') or article['source']['name'].lower().replace(' ', '-'),
                    'id': None
                }
                for article in response['articles']
            }

            for source in unique_source_names.items():
                source_obj, source_created = Source.objects.get_or_create(
                    name=source[0], slug=source[1]['slug'])
                source[1]['id'] = source_obj.id
                print(source)
                print(source_obj.id)

            print('Get or create articles')
            for article in response['articles']:
                print(article)
                article_source_name = article['source']['name']
                article_source_id = unique_source_names[article_source_name]['id']

                article_obj, article_created = Article.objects.get_or_create(
                    url=article['url'],
                    defaults={
                        'source_id': article_source_id,
                        'title': article['title'],
                        'author': article['author'] or '',
                        'description': article['description'] or '',
                        'image_url': article['urlToImage'] or '',
                        'published_at': datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                    }
                )
                print(article_obj.id)
                print(f'created - {article_created}')

    except Exception as e:
        print(str(e))


class Command(BaseCommand):
    help = 'Fetch articles from NewsAPI'

    def handle(self, *args, **options):
        fetch_and_store_articles()
