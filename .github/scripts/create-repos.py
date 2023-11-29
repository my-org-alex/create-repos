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
        
        print("Environments:")
        for env in repo["environments"]:
            print(f"  {env['env_name']}, Production: {env['production']}")
            env_name = (f"{env['env_name']}")
            
            env_data = {
            "wait_timer": 0,
            "prevent_self_review": False
            }

            headers = {
                "Authorization": f"token {ACCESS_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            endpoint = f"{API_ENDPOINT}/{repo_name}/environments/{env_name}"
            response = requests.put(endpoint, json=env_data, headers=headers)

            if response.status_code == 201:
                print(f"Environment '{env_name}' created successfully.")
            else:
                print(f"Error creating environment '{env_name}'. Status code: {response.status_code}")
                print(response.text)

        print("Repository Variables:")
        for var in repo["repo_variables"]:
            print(f"  {var['repo_var_name']}: {var['value']}")
            var_name = (f"{var['repo_var_name']}")
            var_value = (f"{var['value']}")
            
            var_data = {
            "name": var_name,
            "value": var_value
            }

            headers = {
                "Authorization": f"token {ACCESS_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            endpoint = f"{API_ENDPOINT}/{repo_name}/actions/variables"
            response = requests.post(endpoint, json=var_data, headers=headers)

            if response.status_code == 201:
                print(f"Variable '{var_name}' created successfully.")
            else:
                print(f"Error creating variable '{var_name}'. Status code: {response.status_code}")
                print(response.text)

        print("Repository Secrets:")
        for secret in repo["repo_secrets"]:
            print(f"  {secret['repo_secret_name']}: {secret['value']}")
            secret_name = (f"{secret['repo_secret_name']}")
            secret_value = (f"{secret['value']}")
            
            secret_data = {
            "encrypted_value": secret_value,
            "visibility": "private"
            }

            headers = {
                "Authorization": f"token {ACCESS_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            endpoint = f"{API_ENDPOINT}/{repo_name}/actions/secrets/{secret_name}"
            response = requests.put(endpoint, json=secret_data, headers=headers)

            if response.status_code == 201:
                print(f"Secret '{secret_name}' created successfully.")
            else:
                print(f"Error creating secret '{secret_name}'. Status code: {response.status_code}")
                print(response.text)

make_api_call("https://api.github.com/repos/my-org-alex")