import json

with open("../example-files/repo-example.json", "r") as read_json:
    data = json.load(read_json)

print(read_json)