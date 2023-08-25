from pygooglenews import GoogleNews
import newspaper
import requests

gn = GoogleNews()
term = gn.search('Elon Musk twitter x', when = "24h")
entries = term['entries']


for entry in entries:
  print("Title:", entry['title'])
  link = entry['links'][0]['href']
  response = requests.get(link)

  if response.status_code == 200:
    article = newspaper.Article(link)
    article.download()
    article.parse()
    text = article.text
    print(text)
  else:
    print(f"Failed to retrieve the page for {entry['title']}")
  print("-----------------------------------------------")
  