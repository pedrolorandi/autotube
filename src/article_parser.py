import newspaper
import requests
import re

def parse_article_from_link(link):
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        article = newspaper.Article(link)
        article.set_html(response.content)
        article.parse()
    
        text = article.text
        text = re.sub(r'\n+', '', text)
        text = re.sub(r'\s*Advertisement\s*', '', text)
        
        return text
    
    except requests.RequestException as e:
        print(f"Failed to fetch {link} due to error: {e}")
    except Exception as e:
        print(f"An error occurred while processing the article: {e}")

    return None
