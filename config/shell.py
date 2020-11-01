import datetime
import json
import logging
import os
import sys

import django

logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def print_header():
    header = """
      _   _                                    _            _  _
   __| | (_)  __ _  _ __    __ _   ___    ___ | |__    ___ | || |
  / _` | | | / _` || '_ \  / _` | / _ \  / __|| '_ \  / _ \| || |
 | (_| | | || (_| || | | || (_| || (_) | \__ \| | | ||  __/| || |
  \__,_|_/ | \__,_||_| |_| \__, | \___/  |___/|_| |_| \___||_||_|
       |__/                |___/
    """
    print(header)
    print("")


# Helper functions.
def dumps(data):
    print(json.dumps(data, indent=2))


# -------------------------------------------------------------------
# Main entrypoint.
# -------------------------------------------------------------------

# The path of the project, relative to this script.
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    sys.path.insert(0, PROJECT_PATH)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    # -------------------------------------------
    # Imports
    # -------------------------------------------

    # Import django modules.
    from django.conf import settings
    from django.db.models import Avg, Count, Max, Min, Sum, Q
    from django.utils import timezone

    # Import models.
    from articles.models import Article, Source

    # Import other modules.
    from articles.forms import ArticleForm, SourceForm, strip_tags_and_format
    from articles.clients import BingClient, ClientFactory, NewsApiClient
    from articles.actions import ArticlePipeline

    factory = ClientFactory()
    n = factory.get_client('NewsApi')
    b = factory.get_client('Bing')

    n_params = {
        'qintitle': 'daca',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 100,
        'page': 1,
        'from_param': (datetime.date.today() - datetime.timedelta(days=3)).strftime('%Y-%m-%d'),
        'to': datetime.date.today().strftime('%Y-%m-%d')
    }

    b_params = {
        'q': 'daca',
        'textFormat': 'HTML',
        'mkt': 'en-US',
        'count': 100,
        'offset': 0,
        'sortBy': 'Date',
        'max_pages': 1  # Internal param for pagination
    }

    np = ArticlePipeline(n)
    bp = ArticlePipeline(b)

    # -------------------------------------------
    # Entrypoint
    # -------------------------------------------

    print_header()


'''
python -i shell.py
'''
