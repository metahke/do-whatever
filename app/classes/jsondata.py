import json


class JsonData():
    def __init__(self, path):
        self.path = path
        self.data = self.load()

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def get(self, key):
        return self.data[key]

    def add(self, key, value):
        self.data[key].append(value)
