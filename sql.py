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

INSERT_INTO_ARTICLES_TABLE = (
    'INSERT INTO articles (source_id, source_name, author, title, description, url, image_url, published_at, content, created_at) '
    'VALUES (:source_id, :source_name, :author, :title, :description, :url, :urlToImage, :publishedAt, :content, :created_at)'
)
