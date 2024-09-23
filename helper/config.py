import yaml

class config:
    def __init__(self, file_path):
        self.data = self.read_yaml(file_path)

    def read_yaml(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data

    def get(self, *keys):
        result = self.data
        for key in keys:
            result = result[key]
        return result
