from .state import StateHandler
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import pprint

def robot():
  # Initialize state handler and load content
  handler = StateHandler()
  content = handler.load()

  # Load the .env file
  load_dotenv()

  # API Info
  cse_api_key = os.environ.get('GOOGLE_CSE_API_KEY')
  cse_engine_id = os.environ.get('GOOGLE_CSE_ENGINE_ID')

  for sentence in content['sentences']:
    # keywords =  ' '.join(sentence['keywords'])
    # searchTerm = content['searchTerm'] + ' ' + keywords

    # TODO Refactor this function, add try/catch, check face

    resource = build(
      'customsearch', 
      'v1', 
      developerKey = cse_api_key
    ).cse()
    
    results = resource.list(
      q = sentence['image_search_query'], 
      cx = cse_engine_id,
      searchType = 'image', 
    ).execute()

    print(sentence['image_search_query'] + ':\n')

    for result in results['items']:
      pprint.pprint(result['link'])
    print("-----------")

    # TODO
    # Get images from results and append to the images list

    # for result in results['items']:
    #   sentence['images'].append(result['link'])

    # pprint.pprint(sentece)