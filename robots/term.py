from .state import StateHandler

def robot():
  handler = StateHandler()
  content = {}
  content['searchTerm'] = "Elon Musk"

  handler.save(content)