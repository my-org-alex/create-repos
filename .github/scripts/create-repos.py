import json

with open(".github/example-files/repo-example.json", "r") as read_json:
    data = json.load(read_json)

print(read_json)