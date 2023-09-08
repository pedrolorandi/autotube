# Importing necessary modules and classes
from robots import term_robot, text_robot, audio_robot, StateHandler

# Define a dictionary of robots, mapping their names to their respective functions
robots = {
  'term': term_robot,
  'text': text_robot,
  'audio': audio_robot
}

def start():

  # robots['term']()
  robots['text']()
  # robots['audio']()

  # Instantiate the StateHandler to handle the content's state
  handler = StateHandler()

  # Load the content using the StateHandler
  content = handler.load()

  # Print the loaded content
  print(content)

# Check if this script is executed as the main module
if __name__ == "__main__":
  # Print a message indicating the start of the process
  print("Process started")
  
  # Begin the defined process by calling the start function
  start()
