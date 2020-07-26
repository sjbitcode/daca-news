import datetime
import os
import pytz
import uuid

from django.db import transaction
from huey import crontab
from huey.contrib.djhuey import (
    db_periodic_task, db_task,
    periodic_task, task
)
from newsapi import NewsApiClient

from .models import Article, Source


newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_KEY'))
source_ids = [
    'abc-news', 'associated-press', 'cnn', 'fox-news', 'google-news', 'national-review',
    'nbc-news', 'newsweek', 'new-york-magazine', 'politico', 'the-american-conservative',
    'the-hill', 'the-huffington-post', 'the-wall-street-journal', 'the-washington-post',
    'the-washington-times', 'time', 'usa-today', 'wired'
]

# @periodic_task(crontab(minute='*/1'))
# def say_hello():
#     print('Hello, this is a task')


# @db_periodic_task(crontab(minute='*/1'))
# def every_five_mins():
#     rand_str = str(uuid.uuid1())[:5]
#     s = Source(name=f'Some source {rand_str}', name_slug=f'source-{rand_str}')
#     s.save()

# make this periodic!
@db_task()
def fetch_and_store_articles():
    try:
        response = newsapi.get_everything(
            qintitle='daca',
            language='en',
            sources=','.join(source_ids),
            sort_by='relevancy',
            from_param=(datetime.date.today() -
                        datetime.timedelta(days=10)).strftime('%Y-%m-%d'),
            to=datetime.date.today().strftime('%Y-%m-%d')
        )

        print(f"Found {response['totalResults']} articles")

        with transaction.atomic():
            print('Get or create sources')
            unique_source_ids = {article['source']['id']: {'name': article['source']['name']} for article in response['articles']}
            for source in unique_source_ids.items():
                source_obj, source_created = Source.objects.get_or_create(slug=source[0], name=source[1]['name'])
                source[1]['id'] = source_obj.id
                print(source)
                print(source_obj.id)

            print('Get or create articles')
            for article in response['articles']:
                print(article)
                article_source_slug = article['source']['id']
                article_source_id = unique_source_ids[article_source_slug]['id']

                article_obj, article_created = Article.objects.get_or_create(
                    url=article['url'],
                    defaults={
                        'source_id': article_source_id,
                        'title': article['title'],
                        'author': article['author'],
                        'content': article['content'] or '',
                        'description': article['description'] or '',
                        'image_url': article['urlToImage'] or '',
                        'published_at': datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
                    }
                )
                print(article_obj.id)
                print(f'created - {article_created}')

    except Exception as e:
        print(str(e))