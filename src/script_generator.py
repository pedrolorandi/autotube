import os
import re
import openai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def create_script_from_articles(content):
  # API keys
  # openai.organization = os.environ.get('OPENAI_ORG_ID')
  # openai.api_key = os.environ.get('OPENAI_API_KEY')

  # user_prompt = content + "With the information provided, write a youtube script using informal, opinionated, and somewhat satirical tone. Use casual language and often employ sarcasm to make points. Use a sense of skepticism towards media narratives and a desire to present a more down-to-earth perspective on events. The tone should be somewhat confrontational at times, challenging conventional ideas and encouraging the audience to think critically. Overall, the tone should be a blend of commentary, critique, and humor. To add pauses in the script, add a simple dash (-) or the em-dash (—). The script should contain 2000 words. Don't write introduction and conclusion paragraphs. WRITE THE SPEAKING PART ONLY."

  print("Creating script")
  # response = openai.ChatCompletion.create(
  #     model="gpt-4",
  #     temperature=1,
  #     messages=[
  #       {"role": "user", "content": user_prompt}
  #     ]
  # )

  # return response.choices[0].message.content
  
  response = """Well, well, what do we have here? If it isn't our favorite billionaire venture capitalist, "Twitter but without the Twit" enthusiast, and casual intergalactic travel expert, Elon Musk making yet another spectacle, this time at the Valorant World Championship Final. Yes, the very same Musk who decided one day, "Hmmm, what should I do today? I know! I will buy Twitter and rename it to X. Yeah, that'll be fun."

So, our dear Elon shows up at this e-sports event, probably expecting roses to be thrown at him, right? Wrong! If you've seen the clip that's going viral (you know courtesy of the site he renamed), our boy gets booed."""

  print("Creating paragraphs")
  paragraphs = re.split(r'(?<=[.?!])(\s+|\Z)', response)
  
  print("Creating phrases")
  phrases = [segment.strip() for segment in paragraphs if segment]

  print("-----------------------------------------------")
  return phrases
   