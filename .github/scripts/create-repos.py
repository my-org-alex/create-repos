import json

repositories = []
with open('.github/example-files/repo-example.json') as json_file:
    for object in json_file:
        repository = json.loads(object)
        repositories.append(repository)

for repository in repositories:
    print(repository["repo_name"])