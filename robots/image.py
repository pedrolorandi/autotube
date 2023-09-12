from .state import StateHandler
import os

def robot():
  # Initialize state handler and load content
  handler = StateHandler()
  content = handler.load()