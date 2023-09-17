from pygooglenews import GoogleNews
from dotenv import load_dotenv
from .state import StateHandler
from newspaper import Article
import requests
import re
import os
import openai
import nltk
from nltk.tokenize import sent_tokenize

load_dotenv()

nltk.download('punkt')

def robot():
  # Initialize state handler and load content
  handler = StateHandler()
  content = handler.load()  

  # Set OpenAI API credentials
  openai.organization = os.environ.get('OPENAI_ORG_ID')
  openai.api_key = os.environ.get('OPENAI_API_KEY')

  def fetch_news(query, duration="24h"):
    """Fetches news articles based on the query and duration provided.
    
    Parameters:
    - query (str): The search query for fetching news articles.
    - duration (str): The time duration for which to fetch news articles.

    Returns:
    - None
    """
    print("Fetching news...")

    try:
      # Initialize GoogleNews client
      gn = GoogleNews()

      # Search for news articles using the provided query and duration
      search = gn.search(query, when=duration)
      entries = search['entries']

      # Store the top 10 news entries in the content dictionary
      content['entries'] = [
          {'title': entry['title'], 'link': entry['link']}
          for entry in entries[:10]
      ]
    except Exception as e:
      # Handle any exception that occurs during the news fetching process
      print(f"An error occurred while fetching the news: {e}")
    else:
      # Confirm the successful completion of the news fetching process
      print("News fetching complete.\n---")

  def parse_news(content):
    """Parses the news articles from the links stored in the content dictionary.
    
    Parameters:
    - content (dict): The content dictionary storing the news data.

    Returns:
    - None
    """
    print("Parsing news...")

    # Compiling regex patterns to clean the article text
    newline_regex = re.compile(r'\n+')
    adv_regex = re.compile(r'\s*Advertisement\s*')

    valid_articles_count = 0
    content['articles'] = []

    # Loop through the entries and stop after fetching 5 valid articles
    for entry in content.get('entries', []):
      if valid_articles_count >= 5:
        break

      print("Title:", entry['title'])

      try:
        # Attempting to fetch the article content
        response = requests.get(entry['link'], timeout = 10)
        response.raise_for_status()

        # Initializing a newspaper Article object and setting the HTML content
        article = Article(entry['link'])
        article.set_html(response.content)
        article.parse()

        # Cleaning the fetched article text by removing newline characters and advertisement text
        text = article.text
        text = newline_regex.sub('', text)
        text = adv_regex.sub('', text)

        # Appending the cleaned text and title to the articles list
        content['articles'].append({'title': entry['title'], 'text': text})
        valid_articles_count += 1
        print("Article added")
      except requests.RequestException as e:
        print(f"Failed to fetch {entry['link']} due to error: {e}")
      except Exception as e:
        # Catching any other exceptions that may occur during the article processing
        print(f"An error occurred while processing the article: {e}")

      print("---")
    
    print("News parsing complete.\n---")

  def generate_content(content):
    """Generates a single string containing all article content.
    
    Parameters:
    - content (dict): The content dictionary storing the news data.

    Returns:
    - None
    """
    print("Generating content...")

    # Check if there are any articles present in the content dictionary
    if not content.get('articles'):
      print("No articles to generate content from.")
      content['content'] = ""
      return

    # Joining the title and text of each article with a separator to form a single string
    content['content'] = " | ".join(
      f"Title: {article['title']}. {article['text']}"
      for article in content['articles']
    )

    print("Content generation complete.\n---")

  def generate_script(content):
    """
    Generates a YouTube script using OpenAI's GPT-4 based on the parsed and concatenated news content.

    The generated script follows specific tone and content guidelines described in the user prompt.
    The script is stored in the 'script' key in the content dictionary.

    Parameters:
    content (dict): Dictionary holding various pieces of information, including the content based on which the script will be generated.

    Returns:
    None: Modifies the content dictionary in place to add the generated script.
    """
    print("Generating script, please wait...")

    # Formulating the prompt with guidelines for the script generation
    user_prompt = (
      f"{content['content']}"
      "With the information provided, write a youtube script using informal, opinionated, and somewhat satirical tone."
      "Use casual language and often employ sarcasm to make points."
      "Use a sense of skepticism towards media narratives and a desire to present a more down-to-earth perspective on events."
      "The tone should be somewhat confrontational at times, challenging conventional ideas and encouraging the audience to think critically."
      "Overall, the tone should be a blend of commentary, critique, and humor."
      "To add pauses in the script, add a simple dash (-) or the em-dash (—)."
      "The script should contain 3000 words. Don't write introduction and conclusion paragraphs."
      "Don't welcome back people to the channel, and don't use conclusive phrases like 'See you next time'."
      "WRITE THE SPEAKING PART ONLY."
    ) 
    
    try:
      # Making a request to the OpenAI API to generate the script
      response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=1,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
      )

      # Checking the response and extracting the script if the response is valid
      if response and response.choices:
        content['script'] = response.choices[0].message.content
      else:
        raise ValueError("Unexpected response format from OpenAI API")
    except Exception as e:
      # Handling any exceptions that occur during the script generation
      print(f"Failed to generate script due to OpenAI API error: {e}")
      return
 
    print("Script generation complete.\n---")

  def generate_sentences(content):
    """
    Processes a script stored in the 'script' key of the input dictionary to generate a list of sentences, which is then stored back in the input dictionary under the 'sentences' key. Short sentences (less than or equal to 5 words) are merged with the following sentence. Each sentence is stored as a dictionary with keys 'id', 'text', 'keywords', and 'images'.

    Parameters:
    content (dict): A dictionary that contains at least the 'script' key holding the script text to be broken down into sentences. The script is a single string where sentences are separated by full stops.

    Returns:
    None: This function modifies the input dictionary in place, adding a 'sentences' key that holds the generated sentences. Each sentence is represented as a dictionary with an 'id' (the index of the sentence), 'text' (the sentence itself), 'keywords' (an empty list), and 'images' (an empty list).
    """
    print("Generating sentences...")

    # Check if script is None or empty and handle it appropriately
    script = content.get('script')
    if not script:
      print("No script found to generate sentences.")
      content['sentences'] = []
      return

    sentences = sent_tokenize(script)
    sentence_count = len(sentences)
    threshold = 5
    merged_sentences = []
    i = 0

    while i < sentence_count:
      if len(sentences[i].split()) <= threshold and i < len(sentences) - 1:
        merged_sentences.append(sentences[i] + " " + sentences[i + 1])
        i += 2
      else:
        merged_sentences.append(sentences[i])
        i += 1

    content['sentences'] = [
      {'id': idx, 'text': sentence, 'keywords': [], 'images': []}
      for idx, sentence in enumerate(merged_sentences)
    ]

    print("Sentences generation complete.\n---") 

  def generate_search_query(content):
    """
    For each sentence in the 'sentences' list of the input dictionary `content`, this function extracts keywords using OpenAI's GPT-4 model and stores them in a new key called 'image_search_query'.

    Parameters:
    content (dict): A dictionary containing various information, including a 'sentences' key which holds a list of dictionaries representing individual sentences with their respective details.

    Returns:
    None: This function modifies the input dictionary in place to include a 'image_search_query' key in each sentence dictionary with the corresponding extracted keywords.
    """
    print("Generating image search query...")

    # Looping through each sentence in the content dictionary to extract keywords
    for idx, sentence in enumerate(content['sentences']):
      # Crafting a prompt for the GPT-4 model to instruct it to generate an image search query based on the sentence text
      user_prompt = (
        f"Write an image search query to search for an image that illustrates the following sentence: {sentence['text']}."
        "Return only the search query."
      )
      
      try:
        # Making a request to the OpenAI API generate a search query
        response = openai.ChatCompletion.create(
          model="gpt-4",
          temperature=0.5,
          messages=[
              {"role": "user", "content": user_prompt}
          ]
        )

        # Storing the extracted image search query in the 'image_search_query' key of the sentence dictionary
        sentence['image_search_query'] = response.choices[0].message.content.replace('"', '')
      except Exception as e:
        # Handling any exceptions that occur during the image search query generation
        print(f"Failed to generate search term for sentence {idx} due to OpenAI API error: {e}")
        sentence['image_search_query'] = []
        
      print(f"Image search query for sentence {idx} completed.")
    
    print("Image search query generation complete.\n---")

  # Execution of all functions
  # fetch_news(content['searchTerm'])
  # parse_news(content)
  # generate_content(content)
  # generate_script(content)
  # generate_sentences(content)
  generate_search_query(content)

  # Save the modified content back using the handler
  handler.save(content)