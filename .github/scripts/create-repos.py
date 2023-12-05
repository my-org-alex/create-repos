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

class Repository:
    def __init__(self, name):
        self.__name = name

    def create_repo(self, org, access_token):
        repo_name = self.__name

        headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
        }

        data = {
                "name": repo_name,
                "auto_init": True,
                "private": False
            }

        response = requests.post(f"https://api.github.com/orgs/{org}/repos", json=data, headers=headers)

        if (response.status_code == 200 or response.status_code == 201):
            print(f"Repository '{repo_name}' created successfully.")
        else:
            print(f"Error creating repository '{repo_name}'. Status code: {response.status_code}")
            print(response.text)

class Environment:
    def __init__(self, name):
        self.__name = name
    
    def create_environment(self, org, access_token, repo_name):
        env_name = self.__name
        headers = {
                    "Authorization": f"token {access_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
        response = requests.put(f"https://api.github.com/repos/{org}/{repo_name}/environments/{env_name}", headers=headers)
        if (response.status_code == 200 or response.status_code == 201):
            print(f"Environment '{env_name}' created successfully.")
        else:
            print(f"Error creating environment '{env_name}'. Status code: {response.status_code}")
            print(response.text)

class EnvironmentSecret:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value
    
    def create_env_secret(self, org, access_token, repo_name, env_name):
        secret_name = self.__name
        value = self.__value
        
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        get_public_key = requests.get(f"https://api.github.com/repos/{org}/{repo_name}/actions/secrets/public-key", headers=headers)
        json_data = get_public_key.json()
        public_key = json_data["key"]
        public_key_id = json_data["key_id"]
        encrypted_value = encrypt(public_key , value)

        secret_data = {
        "encrypted_value": encrypted_value,
        "key_id": public_key_id
        }

        repo_info = requests.get(f"https://api.github.com/repos/{org}/{repo_name}", headers=headers)
        repo_info_json = repo_info.json()
        repo_id = repo_info_json["id"]

        endpoint = f"https://api.github.com/repositories/{repo_id}/environments/{env_name}/secrets/{secret_name}"
        response = requests.put(endpoint, json=secret_data, headers=headers)

        if (response.status_code == 200 or response.status_code == 201):
            print(f"Environment Secret '{secret_name}' created successfully.")
        else:
            print(f"Error creating Environment Secret '{secret_name}'. Status code: {response.status_code}")
            print(response.text)


class Variable:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def create_variable(self, org, access_token, repo_name):
        var_name = self.__name
        value = self.__value

        var_data = {
        "name": var_name,
        "value": value
        }

        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        endpoint = f"https://api.github.com/repos/{org}/{repo_name}/actions/variables"
        response = requests.post(endpoint, json=var_data, headers=headers)

        if (response.status_code == 200 or response.status_code == 201):
            print(f"Variable '{var_name}' created successfully.")
        else:
            print(f"Error creating variable '{var_name}'. Status code: {response.status_code}")
            print(response.text)


class Secret:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def create_secret(self, org, access_token, repo_name):
        secret_name = self.__name
        value = self.__value

        get_public_key = requests.get(f"https://api.github.com/repos/{org}/{repo_name}/actions/secrets/public-key", headers=headers)
        json_data = get_public_key.json()
        public_key = json_data["key"]
        public_key_id = json_data["key_id"]
        encrypted_value = encrypt(public_key , value)

        secret_data = {
        "encrypted_value": encrypted_value,
        "key_id": public_key_id
        }

        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        endpoint = f"https://api.github.com/repos/{org}/{repo_name}/actions/secrets/{secret_name}"
        response = requests.put(endpoint, json=secret_data, headers=headers)

        if (response.status_code == 200 or response.status_code == 201):
            print(f"Secret '{secret_name}' created successfully.")
        else:
            print(f"Error creating Secret '{secret_name}'. Status code: {response.status_code}")
            print(response.text)
    

def create_repositories(json_file, org):
    access_token = os.environ.get("ACCESS_TOKEN")

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    with open(json_file, 'r') as file:
        content = json.load(file)

    for repo in content["repositories"]:
        repo_name = (f"{repo['repo_name']}")
        repository = Repository(repo_name)

        repo_exists = requests.get(f"https://api.github.com/repos/{org}/{repo_name}", headers=headers)

        if repo_exists.status_code == 404:
            repository.create_repo(org, access_token)

            for env in repo["environments"]:
                env_name = (f"{env['env_name']}")
                environment = Environment(env_name)
                environment.create_environment(org, access_token, repo_name) 

                for secret in env["env_secrets"]:
                    secret_name = (f"{secret['env_secret_name']}")
                    secret_value = (f"{secret['value']}")

                    env_secret = EnvironmentSecret(secret_name, secret_value)
                    env_secret.create_env_secret(org, access_token, repo_name, env_name)
                    
            for var in repo["repo_variables"]:
                var_name = (f"{var['repo_var_name']}")
                var_value = (f"{var['value']}")
                
                repo_var = Variable(var_name, var_value)
                repo_var.create_variable(org, access_token, repo_name)

            for secret in repo["repo_secrets"]:
                secret_name = (f"{secret['repo_secret_name']}")
                secret_value = (f"{secret['value']}")

                repo_secret = Secret(secret_name, secret_value)
                repo_secret.create_secret(org, access_token, repo_name)
        else:
            print(f"Repository {repo_name} already exists!")

create_repositories('.github/example-files/repo-example.json', "my-org-alex")