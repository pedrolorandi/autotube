from pygooglenews import GoogleNews
from dotenv import load_dotenv
import newspaper
import requests
import re
import os
import openai
import json

def robot(content):
  def fetch_news(query, duration="24h"):
    print("Fetching news")

    gn = GoogleNews()
    search = gn.search(query, when=duration)
    entries = search['entries']
    
    content['entries'] = []

    for entry in entries[:10]:
      new_entry = {
          'title': entry['title'],
          'link': entry['link']
      }

      content['entries'].append(new_entry)

    print("News fetching complete.\n---")

  def parse_news(content):
    print("Parsing news")

    valid_articles_count = 0
    content['articles'] = []

    for entry in content['entries']:
      if valid_articles_count == 5:
        break
  
      print("Title:", entry['title'])

      try:
        response = requests.get(entry['link'], timeout=10)
        response.raise_for_status()
        
        article = newspaper.Article(entry['link'])
        article.set_html(response.content)
        article.parse()
    
        text = article.text
        text = re.sub(r'\n+', '', text)
        text = re.sub(r'\s*Advertisement\s*', '', text)
        
        new_article = {
          'title': entry['title'],
          'text': text
        }

        content['articles'].append(new_article)
        valid_articles_count += 1

        print("Article added")
    
      except requests.RequestException as e:
          print(f"Failed to fetch {entry['link']} due to error: {e}")
      except Exception as e:
          print(f"An error occurred while processing the article: {e}")

      print("---")

    print("News parsing complete.\n---")

  def generate_content(content):
    print("Generating content")

    full_content = ""

    for article in content['articles']:
      full_content += "Title: " + article['title'] + "."
      full_content += article['text'] + " | "

    content['content'] = full_content

    print("Content generation complete.\n---")

  def generate_script(content):
    print("Generating script")

    # Load the .env file
    load_dotenv()

    # API keys
    openai.organization = os.environ.get('OPENAI_ORG_ID')
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    user_prompt = content['content'] + "With the information provided, write a youtube script using informal, opinionated, and somewhat satirical tone. Use casual language and often employ sarcasm to make points. Use a sense of skepticism towards media narratives and a desire to present a more down-to-earth perspective on events. The tone should be somewhat confrontational at times, challenging conventional ideas and encouraging the audience to think critically. Overall, the tone should be a blend of commentary, critique, and humor. To add pauses in the script, add a simple dash (-) or the em-dash (—). The script should contain 2000 words. Don't write introduction and conclusion paragraphs. Don't welcome back people to the channel, and don't use conclusive phrases like 'See you next time'. WRITE THE SPEAKING PART ONLY."

    response = openai.ChatCompletion.create(
        model = "gpt-4",
        temperature = 1,
        messages = [
          {"role": "user", "content": user_prompt}
        ]
    )

    content['script'] = response.choices[0].message.content
#     content['script'] = '''Alright guys, hold onto your hats... this is a juicy one. So the billionaire boys' club is squaring off again, with old rivalries threatening to become litigious. Jeff Bezos, Amazon overlord, and Elon Musk, the Tesla tycoon, are apparently in a tiff about who gets to litter low-Earth orbit with their internet satellites.

# So here’s what went down: the Amazon bigwigs came up with this bright idea called Project Kuiper, which is all about launching a bunch of satellites to provide internet services, right? The deal's worth billions - I mean, why wouldn't it be when the Beards are involved? Anyway, Bezos and his team decided to bring some companies on board for this space shindig.

# Who did they call up? Well, there's the United Launch Alliance - that's Boeing and Lockheed Martin, in case you don't have your space industry scorecard handy. Next is European Arianespace and finally, Bezos's own pet project, Blue Origin. Somebody must have missed the memo on conflict of interest there, right?

# Now, you'd think our main man Elon Musk and his interstellar venture SpaceX will be right up there in that lineup. I mean, Elon is the de facto poster boy for commercial spaceflight. But no. Elon got left on read.

# Wait up - you're telling me the company that's already flung something like 5,000 satellites into space for its own internet service, Starlink, wasn't even considered for a shot at this thing? It's like hosting a hot dog eating contest and not inviting Joey Chestnut.

# And now, Amazon shareholders are crying foul play. They're claiming Bezos's personal beef with Musk led to SpaceX's snub from Project Kuiper. The Amazon leaders are being accused of wagging their schoolyard rivalry all over a billion-dollar contract.

# Seriously, the whole spat is starting to sound like a space-themed telenovela—complete with screenshots of the pair's public sniping on X - the platform formerly known as Twitter - being included in the lawsuit filing.

# Anyway, Amazon has decided to shrug this off like a bad smell. They say the lawsuit is without merit. What, and I'm Jeff Bezos's less affluent cousin, right?

# Would you believe it, it's not even clear if SpaceX submitted a bid for the work or showed any interest in helping a rival launch their own satellites. But this is Musk we're talking about - I mean, do we really think he'd pass up an opportunity to further his space conquest and tussle with Bezos at the same time?

# But this lawsuit isn't just about the Bezos-Musk face-off. It seems that Bezos' close ties to both Amazon and Blue Origin are raising more than a few eyebrows. Guess sitting on the throne of both castles has its downsides, huh?

# Folks won't let it slide that Bezos and his crew barely gave the contract’s terms a once-over before they whipped out the big "approved" stamp. Talk about a rushed job. The shareholders claim that the committee had no information about how Bezos and his team negotiated with Blue Origin, nor about Bezos' involvement or how many other launch providers they considered working with.

# And wouldn’t you just know it, the suit also brings up the shady past of Blue Origin's contracts. Remember earlier this year when reports revealed that one of their New Glenn rockets went all Fourth of July during testing? Yeah, apparently, that's the same rocket slated to land for a $3.4 billion NASA project. Whoops.

# But wait, there's more drama. We circle back to Musk and his list of frenemies in the tech industry, with Bezos being one of his oldest and perhaps favorite adversaries. I mean, Musk has gone so far as to call for Amazon to be broken up, labeling it a "monopoly". Yeah, because Tesla and SpaceX are corner-shop businesses, right Elon?

# Their online taunting and jabbing have become something of a spectator sport for us mere mortals. Take the time when Musk called out Bezos for copying SpaceX's plans, or when he straight-up told Bezos to "sue your way to the moon".

# So here we are folks, watching the billionaires duke it out in court - it's like a reality show, but with rockets and the future of the internet hanging in the balance. You couldn't make this stuff up.'''

    print("Script generation complete.\n---")

  def generate_sentences(content):
    print("Generating sentences")

    sentences = re.split(r'\n{2,}', content['script'])

    content['sentences'] = []

    for idx, sentence in enumerate(sentences):
      new_sentence = {
        'id': idx,
        'text': sentence,
        'keywords': [],
        'images': []
      }

      content['sentences'].append(new_sentence)
    print("Sentences generation complete.\n---")

  def generate_keywords(content):
    print("Generating keywords")

    # Load the .env file
    load_dotenv()

    # API keys
    openai.organization = os.environ.get('OPENAI_ORG_ID')
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    for idx, sentence in enumerate(content['sentences'][:1]):
      user_prompt = "Return a string with the 6 main keywords and/or entities separated by ' ' from following text: " + sentence['text']

      response = openai.ChatCompletion.create(
          model = "gpt-3.5-turbo",
          temperature = 0.5,
          messages = [
            {"role": "user", "content": user_prompt}
          ]
      )
      
      sentence['keywords'] = response.choices[0].message.content
      print(f"Keywords for sentence {idx} completed.")

    print("Keywords generation complete.\n---")

  fetch_news(content['searchTerm'])
  parse_news(content)
  generate_content(content)
  generate_script(content)
  generate_sentences(content)
  generate_keywords(content)