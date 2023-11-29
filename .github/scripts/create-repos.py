import os
import json
import requests

def make_api_call(endpoint):
    JSON_FILE = '.github/example-files/repo-example.json'
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    API_ENDPOINT = endpoint

    print(API_ENDPOINT)

    with open(JSON_FILE, 'r') as file:
        content = json.load(file)

    for repo in content["repositories"]:
        repo_name = (f"{repo['repo_name']}")

        data = {
            "name": repo_name,
            "auto_init": True,
            "private": False
        }

        headers = {
            "Authorization": f"token {ACCESS_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.post(API_ENDPOINT, json=data, headers=headers)

        if response.status_code == 201:
            print(f"Repository '{repo_name}' created successfully.")
        else:
            print(f"Error creating repository '{repo_name}'. Status code: {response.status_code}")
            print(response.text)

make_api_call("https://api.github.com/orgs/my-org-alex/repos")
    
    # print("Environments:")
    # for env in repo["environments"]:
    #     print(f"  {env['env_name']}, Production: {env['production']}")

    # print("Repository Variables:")
    # for var in repo["repo_variables"]:
    #     print(f"  {var['repo_var_name']}: {var['value']}")

    # print("Repository Secrets:")
    # for secret in repo["repo_secrets"]:
    #     print(f"  {secret['repo_secret_name']}: {secret['value']}")