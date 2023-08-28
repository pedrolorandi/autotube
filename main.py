import os
from dotenv import load_dotenv
from src import fetch_news_articles, parse_article_from_link

# Load the .env file
load_dotenv()

# API keys
openai_api_key = os.environ.get('OPENAI_API_KEY')

entries = fetch_news_articles('twitter')
content = ''

for entry in entries[:5]:
    print("Title:", entry['title'])
    link = entry['links'][0]['href']
    article_text = parse_article_from_link(link)
    
    if article_text:
        content += "Title: " + entry['title'] + "."
        content += article_text + "\n-\n"
        print("Article added")
    else:
        print(f"Failed to retrieve the page for {entry['title']}")
    
    print("-----------------------------------------------")
    print(content)