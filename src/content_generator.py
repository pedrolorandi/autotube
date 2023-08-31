from .news_fetcher import fetch_news_articles
from .article_parser import parse_article_from_link

def create_content_from_articles(topic, max_articles):
    
  entries = fetch_news_articles(topic)
  content = ''
  valid_articles_count = 0

  for entry in entries:
    # Break once we've fetched the desired number of valid articles
    if valid_articles_count == max_articles:
        break

    print("Title:", entry['title'])
    link = entry['links'][0]['href']
    article_text = parse_article_from_link(link)
    
    if article_text:
        content += "Title: " + entry['title'] + "."
        content += article_text + "\n-\n"
        print("Article added")
        print(valid_articles_count)
        valid_articles_count += 1
    else:
        print(f"Failed to retrieve the page for {entry['title']}")

    print("-----------------------------------------------")
  
  return content