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

  # user_prompt = content + "With the information provided, write a youtube script using informal, opinionated, and somewhat satirical tone. Use casual language and often employ sarcasm to make points. Use a sense of skepticism towards media narratives and a desire to present a more down-to-earth perspective on events. The tone should be somewhat confrontational at times, challenging conventional ideas and encouraging the audience to think critically. Overall, the tone should be a blend of commentary, critique, and humor. The script should contain 2000 words. Don't write introduction and conclusion paragraphs. WRITE THE SPEAKING PART ONLY."

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

So, our dear Elon shows up at this e-sports event, probably expecting roses to be thrown at him, right? Wrong! If you've seen the clip that's going viral (you know courtesy of the site he renamed), our boy gets booed. Not by one, not two, but by the entire crowd. And oh boy, the sweet irony that the guy who basically owns the primary platform for online jeering gets served the same dish in real life.

So he's sitting there, doing his billionaire thing, clapping for... something or maybe just to drown the boos, who knows? And the entire crowd starts chanting "Bring back Twitter!" I mean, can you imagine the look on his face? I bet he didn't see that one coming, although to be fair, he probably couldn't hear it over his own clapping. And bless the commentators who were desperately trying to steer the crowd back to the game with a confused, "Where is that from? That can't be from in here, surely?" Yeah mate, wishful thinking.

And you know the part I love the most? When one of these commentators makes a snide comment about Musk's reaction being bigger than that of professional Valorant player "tenZ." Like how's that for a reality check, Elon? You are at a sports tournament and the crowd is more interested in booing you than cheering for the players. Now that's a memory to take home.

Just when you think it couldn't get better, the crowd starts chanting "Bring back Twitter" again. And by better, I mean painfully embarrassing, obviously. Couldn't help but be impressed by the consistency, tbh. And then there are these comments on X, one user even comparing the whole episode to "getting wedgies by the anime club in middle school." And man, I've got to say, that Twitter, sorry X tweet has got some punch to it.

But wait! There's more! Remember when Dave Chappelle brought Musk on stage last December? You got it - booed yet again. But according to Musk, it was apparently 90% cheers and 10% boos except during the quiet periods. Now I don't know what video he's been watching but the only cheers I heard were perhaps cheers of joy at the sweet nectar of public accountability being served to ol' Musk.

Now, let's change gears a little and talk about this whole renaming Twitter to X debacle. So, Musk wakes up one morning and decides, "Twitter? Nah, Twitter's overrated. Let's go for X, the unknown." What's next? Are we changing the name of Earth to Y? And how's that rebrand going for you, Musk? Last I heard, the site was temporarily blocked in Indonesia because of the country's anti-porn and gambling laws. Maybe should've thought about researching potential namesakes before finalizing on one, huh?

As for the company's value, it's estimated that the name change itself could make the company's value drop anywhere from $4 billion to $20 billion. Ouch. A $20 billion worth facepalm? That's got to hurt. As for the brands, it seems nobody really got the memo about the name change yet, or maybe they just don't care, who knows?

So, what's the takeaway here? While it's quite amusing to toss all these jabs at Musk, let's not miss the point. This whole saga sheds a light on how the actions of these billionaires can have real world consequences, and sometimes, those consequences show up in the form of angry gamers booing them at an e-sports tournament. Don't know if Elon will ever bring back Twitter, or if X is here to stay, but one thing's for sure - Valorant gamers have certainly got their priorities straight."""

  print("Creating paragraphs")
  paragraphs = re.split(r'(?<=[.?!])(\s+|\Z)', response)
  
  print("Creating phrases")
  phrases = [segment.strip() for segment in paragraphs if segment]

  print("-----------------------------------------------")
  return phrases
   