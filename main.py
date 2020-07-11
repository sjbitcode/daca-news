import datetime
import os
import sqlite3

from newsapi import NewsApiClient

from sources import source_ids
import sql


# Establish db connection and insert articles.
conn = sql.initialize_db()

# Initialize NewsAPI client.
newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_KEY'))

fetched_articles = newsapi.get_everything(
    qintitle='daca',
    language='en',
    sources=','.join(source_ids),
    sort_by='relevancy',
    from_param=(datetime.date.today() -
                datetime.timedelta(days=10)).strftime('%Y-%m-%d'),
    to=datetime.date.today().strftime('%Y-%m-%d')
)

with conn:
    for article in fetched_articles['articles']:

        # Make source info as attributes on top level of dict.
        article['source_id'] = article['source']['id']
        article['source_name'] = article['source']['name']
        article['created_at'] = datetime.datetime.utcnow().strftime(
            '%Y-%m-%dT%H:%M:%SZ')

        try:
            conn.execute(sql.INSERT_INTO_ARTICLES_TABLE, article)
        except sqlite3.IntegrityError:
            print('Attemtped to insert duplicate article')
        except Exception as e:
            print(str(e))
