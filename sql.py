import sqlite3


ENABLE_FOREIGN_KEYS = 'PRAGMA foreign_keys = ON;'

SQL_CREATE_ARTICLES_TABLE = (
    'CREATE TABLE IF NOT EXISTS articles ('
    'id integer PRIMARY KEY, '
    'source_id TEXT, '
    'source_name TEXT, '
    'author TEXT, '
    'title TEXT, '
    'description TEXT, '
    'url TEXT, '
    'image_url TEXT, '
    'published_at TEXT, '
    'content TEXT, '
    'created_at TEXT, '
    'UNIQUE(url) '
    ');'
)

SQL_CREATE_DIGEST_TABLE = (
    'CREATE TABLE IF NOT EXISTS digest ('
    'id integer PRIMARY KEY, '
    'sent_at TEXT'
    ');'
)

SQL_CREATE_RECIPIENT_TABLE = (
    'CREATE TABLE IF NOT EXISTS recipient ('
    'id integer PRIMARY KEY, '
    'name TEXT, '
    'email TEXT, '
    'UNIQUE(email)'
    ');'
)

SQL_CREATE_ARTICLES_DIGEST_THROUGH_TABLE = (
    'CREATE TABLE IF NOT EXISTS articles_digest ('
    'id integer PRIMARY KEY, '
    'article_id INTEGER NOT NULL, '
    'digest_id INTEGER NOT NULL, '
    'FOREIGN KEY(article_id) REFERENCES articles(id), '
    'FOREIGN KEY(digest_id) REFERENCES digest(id)'
    ');'
)

SQL_CREATE_ARTICLES_RECIPIENT_THROUGH_TABLE = (
    'id integer PRIMARY KEY, '
    'CREATE TABLE IF NOT EXISTS articles_recipient ('
    'article_id INTEGER NOT NULL, '
    'recipient_id INTEGER NOT NULL, '
    'FOREIGN KEY(article_id) REFERENCES articles(id), '
    'FOREIGN KEY(recipient_id) REFERENCES recipient(id)'
    ');'
)

INSERT_INTO_ARTICLES_TABLE = (
    'INSERT INTO articles (source_id, source_name, author, title, description, url, image_url, published_at, content, created_at) '
    'VALUES (:source_id, :source_name, :author, :title, :description, :url, :urlToImage, :publishedAt, :content, strftime("%Y-%m-%dT%H:%M:%SZ"))'
)


def initialize_db():
    sql_setup = (
        f"{ENABLE_FOREIGN_KEYS} "
        f"{SQL_CREATE_ARTICLES_TABLE} "
        f"{SQL_CREATE_DIGEST_TABLE} "
        f"{SQL_CREATE_RECIPIENT_TABLE} "
        f"{SQL_CREATE_ARTICLES_DIGEST_THROUGH_TABLE} "
        f"{SQL_CREATE_ARTICLES_RECIPIENT_THROUGH_TABLE}"
    )
    conn = sqlite3.connect('daca_news.db')
    conn.row_factory = sqlite3.Row
    conn.executescript(sql_setup)
    return conn
