# from newsapi import NewsApiClient
# newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_KEY'))
# sources = newsapi.get_sources(language='en', country='us')


# these are the sources extraced from the above sources endpoint.
sources = [
    {
        'id': 'abc-news',
        'name': 'ABC News',
        'description': 'Your trusted source for breaking news, analysis, exclusive interviews, headlines, and videos at ABCNews.com.',
        'url': 'https://abcnews.go.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'associated-press',
        'name': 'Associated Press',
        'description': 'The AP delivers in-depth coverage on the international, politics, lifestyle, business, and entertainment news.',
        'url': 'https://apnews.com/',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'cnn',
        'name': 'CNN',
        'description': 'View the latest news and breaking news today for U.S., world, weather, entertainment, politics and health at CNN',
        'url': 'http://us.cnn.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'fox-news',
        'name': 'Fox News',
        'description': 'Breaking News, Latest News and Current News from FOXNews.com. Breaking news and video. Latest Current News: U.S., World, Entertainment, Health, Business, Technology, Politics, Sports.',
        'url': 'http://www.foxnews.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'google-news',
        'name': 'Google News',
        'description': 'Comprehensive, up-to-date news coverage, aggregated from sources all over the world by Google News.',
        'url': 'https://news.google.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'national-review',
        'name': 'National Review',
        'description': 'National Review: Conservative News, Opinion, Politics, Policy, & Current Events.',
        'url': 'https://www.nationalreview.com/',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'nbc-news',
        'name': 'NBC News',
        'description': 'Breaking news, videos, and the latest top stories in world news, business, politics, health and pop culture.',
        'url': 'http://www.nbcnews.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'newsweek',
        'name': 'Newsweek',
        'description': 'Newsweek provides in-depth analysis, news and opinion about international issues, technology, business, culture and politics.',
        'url': 'https://www.newsweek.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'new-york-magazine',
        'name': 'New York Magazine',
        'description': 'NYMAG and New York magazine cover the new, the undiscovered, the next in politics, culture, food, fashion, and behavior nationally, through a New York lens.',
        'url': 'http://nymag.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'politico',
        'name': 'Politico',
        'description': 'Political news about Congress, the White House, campaigns, lobbyists and issues.',
        'url': 'https://www.politico.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'the-american-conservative',
        'name': 'The American Conservative',
        'description': 'Realism and reform. A new voice for a new generation of conservatives.',
        'url': 'http://www.theamericanconservative.com/',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'the-hill',
        'name': 'The Hill',
        'description': 'The Hill is a top US political website, read by the White House and more lawmakers than any other site -- vital for policy, politics and election campaigns.',
        'url': 'http://thehill.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'the-huffington-post',
        'name': 'The Huffington Post',
        'description': 'The Huffington Post is a politically liberal American online news aggregator and blog that has both localized and international editions founded by Arianna Huffington, Kenneth Lerer, Andrew Breitbart, and Jonah Peretti, featuring columnists.',
        'url': 'http://www.huffingtonpost.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'the-wall-street-journal',
        'name': 'The Wall Street Journal',
        'description': 'WSJ online coverage of breaking news and current headlines from the US and around the world. Top stories, photos, videos, detailed analysis and in-depth reporting.',
        'url': 'http://www.wsj.com',
        'category': 'business',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'the-washington-post',
        'name': 'The Washington Post',
        'description': 'Breaking news and analysis on politics, business, world national news, entertainment more. In-depth DC, Virginia, Maryland news coverage including traffic, weather, crime, education, restaurant reviews and more.',
        'url': 'https://www.washingtonpost.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'the-washington-times',
        'name': 'The Washington Times',
        'description': 'The Washington Times delivers breaking news and commentary on the issues that affect the future of our nation.',
        'url': 'https://www.washingtontimes.com/',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'time',
        'name': 'Time',
        'description': 'Breaking news and analysis from TIME.com. Politics, world news, photos, video, tech reviews, health, science and entertainment news.',
        'url': 'http://time.com',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'usa-today',
        'name': 'USA Today',
        'description': 'Get the latest national, international, and political news at USATODAY.com.',
        'url': 'http://www.usatoday.com/news',
        'category': 'general',
        'language': 'en',
        'country': 'us'
    },
    {
        'id': 'wired',
        'name': 'Wired',
        'description': 'Wired is a monthly American magazine, published in print and online editions, that focuses on how emerging technologies affect culture, the economy, and politics.',
        'url': 'https://www.wired.com',
        'category': 'technology',
        'language': 'en',
        'country': 'us'
    },
]

source_ids = [source['id'] for source in sources]
