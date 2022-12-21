import json

def readJson(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data