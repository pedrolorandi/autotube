from src import fetch_news_articles, parse_article_from_link, create_script_from_articles, create_audio_from_phrases

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

phrases = create_script_from_articles(content)
audios = create_audio_from_phrases(phrases)