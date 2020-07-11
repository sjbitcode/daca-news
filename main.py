import datetime
import os
import smtplib
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


def send_email():
    """
    Send a test email with the last inserted article.

    Run the following to start up smtp debugging server:
        python -m smtpd -c DebuggingServer -n localhost:5555
    """
    sender = 'sjbitcode@gmail.com'

    # Get all recipients.
    recipients_rows = conn.execute('SELECT email FROM recipient;').fetchall()
    recipients = [row['email'] for row in recipients_rows]

    # Get latest article.
    one_article = conn.execute(
        'SELECT * FROM articles ORDER BY created_at LIMIT 1;').fetchone()
    message = (
        f'Daca article\n'
        f"{one_article['title']}"
        f"{one_article['author']}"
        f"{one_article['url']}"
        f"{one_article['published_at']}"
    )

    try:
        smtpObj = smtplib.SMTP('localhost', 5555)
        smtpObj.sendmail(sender, recipients, message)
        print('Successfully sent email')

    except smtplib.SMTPException:
        print('SMTPLib Error, unable to send email')
    except Exception:
        raise
