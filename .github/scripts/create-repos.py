import os
import json
import requests
from base64 import b64encode
from nacl import encoding, public

def encrypt(public_key: str, secret_value: str) -> str:
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")

def make_api_call(endpoint):
    json_file = '.github/example-files/repo-example.json'
    access_token = os.environ.get("ACCESS_TOKEN")
    api_endpoint = endpoint

    with open(json_file, 'r') as file:
        content = json.load(file)

    for repo in content["repositories"]:
        repo_name = (f"{repo['repo_name']}")
        repo_endpoint = f"https://api.github.com/repos/my-org-alex/{repo_name}"

        data = {
            "name": repo_name,
            "auto_init": True,
            "private": False
        }

        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.post(api_endpoint, json=data, headers=headers)

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
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            endpoint = f"{repo_endpoint}/environments/{env_name}"
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
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            endpoint = f"{repo_endpoint}/actions/variables"
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
            public_key = requests.get(f"{api_endpoint}/actions/secrets/public-key")

            
            secret_data = {
            "encrypted_value": encrypt(public_key , secret_value),
            "key_id": public_key
            }

            headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            endpoint = f"{api_endpoint}/actions/secrets/{secret_name}"
            response = requests.put(endpoint, json=secret_data, headers=headers)

            if response.status_code == 201:
                print(f"Secret '{secret_name}' created successfully.")
            else:
                print(f"Error creating secret '{secret_name}'. Status code: {response.status_code}")
                print(response.text)

make_api_call("https://api.github.com/orgs/my-org-alex/repos")