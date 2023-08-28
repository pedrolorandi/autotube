from pygooglenews import GoogleNews

def fetch_news_articles(query, duration="24h"):
    gn = GoogleNews()
    search = gn.search(query, when=duration)
    entries = search['entries']
    return entries
