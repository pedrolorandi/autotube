import newspaper
import requests
import re

def parse_article_from_link(link):
    response = requests.get(link)
    
    if response.status_code != 200:
        return None
    
    article = newspaper.Article(link)
    article.set_html(response.content)
    article.parse()
    
    text = article.text
    text = re.sub(r'\n+', '', text)
    text = re.sub(r'\s*Advertisement\s*', '', text)
    
    return text