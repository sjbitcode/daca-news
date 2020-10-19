import datetime
import html
import io
import json
import os
import requests

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from articles.models import Article, Source


# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python


class MLStripper(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = io.StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html_str):
    html_str = html.unescape(html_str)
    s = MLStripper()
    s.feed(html_str)
    return s.get_data()


subscription_key = os.environ.get('BING_SUBSCRIPTION_KEY')
search_term = "daca"
search_url = os.path.join(os.environ.get('BING_PROJECT_ENDPOINT'), 'bing/v7.0/news/search')
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
# params = {
#     "q": search_term,
#     "textDecorations": True,
#     "textFormat": "HTML",
#     "mkt": "en-US",
#     "category": "Politics",
#     "count": 40,
#     # "offset": 100,
#     # "freshness": "Month",
#     # "since": 1577836800,
#     "sortBy": "Date"
# }

params = {
    "q": search_term,
    "textFormat": "HTML",
    "mkt": "en-US",
    # "category": "Politics",
    "count": 40,
    "offset": 160,
    # "freshness": "Month",
    # "since": 1577836800,
    "sortBy": "Date"
}


def fetch_and_store_articles():
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        for article in results['value']:
            print(article['name'])
            print(article['datePublished'])
            print(article['provider'])
            print(article['url'])
            print('---')

        print(f'{len(results["value"])} ARTICLES FOUND')
        print(f'api call url - {response.request.url}')

        with open(f'bing_results_{datetime.datetime.now()}.json', 'w') as outfile:
            json.dump(results, outfile)

    except Exception as e:
        print(str(e))


class Command(BaseCommand):
    help = 'Fetch articles from Bing'

    def handle(self, *args, **options):
        fetch_and_store_articles()
