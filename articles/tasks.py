import logging

from huey import crontab
from huey.contrib.djhuey import periodic_task


from articles.actions import (
    bing_pipeline, bing_default_params,
    news_api_pipeline, newsapi_default_params
)

logger = logging.getLogger(__name__)


def fetch_bing_and_newsapi():
    try:
        bing_pipeline.fetch_and_save_articles(params=bing_default_params)
    except Exception as e:
        logger.error(str(e))

    try:
        news_api_pipeline.fetch_and_save_articles(params=newsapi_default_params)
    except Exception as e:
        logger.error(str(e))


@periodic_task(crontab(hour='*/6'))
def perform_fetch_and_store_articles():
    fetch_bing_and_newsapi()
