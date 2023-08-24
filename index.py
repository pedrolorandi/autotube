from pygooglenews import GoogleNews
from bs4 import BeautifulSoup
import requests

gn = GoogleNews()
term = gn.search('Elon Musk', when = "24h")
entries = term['entries']



for entry in entries:
  print("Title:", entry['title'])
  response = requests.get(entry['links'][0]['href'])

  if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.text[:1000])
  else:
    print(f"Failed to retrieve the page for {entry['title']}")
  print("-----------------------------------------------")
  