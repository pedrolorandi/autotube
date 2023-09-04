import json

class StateHandler:
    def __init__(self, file_path = './content.json'):
        self.file_path = file_path

    def save(self, content):
        with open(self.file_path, 'w') as file:
            json.dump(content, file)

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {self.file_path} not found!")
            return {}
