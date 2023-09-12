import json

class StateHandler:
  def __init__(self, file_path = './content.json'):
    # Set the file path for storing and retrieving content
    self.file_path = file_path

  def save(self, content):
    # Open the file in write mode
    with open(self.file_path, 'w') as file:
      # Save the content to the file in JSON format
      json.dump(content, file)

  def load(self):
    try:
      # Open the file in read mode
      with open(self.file_path, 'r') as file:
        # Load and return the content from the file
        return json.load(file)
    except FileNotFoundError:
      # Handle the case where the file is not found
      print(f"File {self.file_path} not found! Creating a new one...")
      self.save({})  # Create a new file with an empty dictionary
      return {}
