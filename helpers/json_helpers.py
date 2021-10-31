import json

def load_json(file_path: str) -> json:
    with open(f'{file_path}.json') as file:
        json_file = json.load(file)
    return json_file