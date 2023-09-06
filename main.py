from robots import term_robot, text_robot, StateHandler

robots = {
  'term': term_robot,
  'text': text_robot
}

def start():
  robots['term']()
  robots['text']()

  handler = StateHandler()
  content = handler.load()

  print(content)

if __name__ == "__main__":
  print("Process started")
  start()