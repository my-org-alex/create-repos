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

def make_api_call(json_file, org, endpoint):
    access_token = os.environ.get("ACCESS_TOKEN")
    api_endpoint = endpoint

    with open(json_file, 'r') as file:
        content = json.load(file)

    for repo in content["repositories"]:
        repo_name = (f"{repo['repo_name']}")
        repo_endpoint = f"https://api.github.com/repos/{org}/{repo_name}"
        
        headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
        }

        repo_exists = requests.get(f"{repo_endpoint}", headers=headers)

        if repo_exists.status_code == 404:
            data = {
                "name": repo_name,
                "auto_init": True,
                "private": False
            }

            response = requests.post(api_endpoint, json=data, headers=headers)

            if (response.status_code == 200 or response.status_code == 201):
                print(f"Repository '{repo_name}' created successfully.")
            else:
                print(f"Error creating repository '{repo_name}'. Status code: {response.status_code}")
                print(response.text)
            
            for env in repo["environments"]:
                env_name = (f"{env['env_name']}")

                headers = {
                    "Authorization": f"token {access_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                endpoint = f"{repo_endpoint}/environments/{env_name}"
                response = requests.put(endpoint, headers=headers)

                if (response.status_code == 200 or response.status_code == 201):
                    print(f"Environment '{env_name}' created successfully.")
                    for secret in env["env_secrets"]:
                        secret_name = (f"{secret['env_secret_name']}")
                        secret_value = (f"{secret['value']}")
                    
                        get_public_key = requests.get(f"{repo_endpoint}/actions/secrets/public-key", headers=headers)
                        json_data = get_public_key.json()
                        public_key = json_data["key"]
                        public_key_id = json_data["key_id"]
                        encrypted_value = encrypt(public_key , secret_value)

                        secret_data = {
                        "encrypted_value": encrypted_value,
                        "key_id": public_key_id
                        }

                        headers = {
                            "Authorization": f"token {access_token}",
                            "Accept": "application/vnd.github.v3+json"
                        }
                        endpoint = f"{repo_endpoint}/actions/secrets/{secret_name}"
                        response = requests.put(endpoint, json=secret_data, headers=headers)

                        if (response.status_code == 200 or response.status_code == 201):
                            print(f"Secret '{secret_name}' created successfully.")
                        else:
                            print(f"Error creating secret '{secret_name}'. Status code: {response.status_code}")
                            print(response.text)
                else:
                    print(f"Error creating environment '{env_name}'. Status code: {response.status_code}")
                    print(response.text)

            for var in repo["repo_variables"]:
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

                if (response.status_code == 200 or response.status_code == 201):
                    print(f"Variable '{var_name}' created successfully.")
                else:
                    print(f"Error creating variable '{var_name}'. Status code: {response.status_code}")
                    print(response.text)

            for secret in repo["repo_secrets"]:
                secret_name = (f"{secret['repo_secret_name']}")
                secret_value = (f"{secret['value']}")
            
                get_public_key = requests.get(f"{repo_endpoint}/actions/secrets/public-key", headers=headers)
                json_data = get_public_key.json()
                public_key = json_data["key"]
                public_key_id = json_data["key_id"]
                encrypted_value = encrypt(public_key , secret_value)

                secret_data = {
                "encrypted_value": encrypted_value,
                "key_id": public_key_id
                }

                headers = {
                    "Authorization": f"token {access_token}",
                    "Accept": "application/vnd.github.v3+json"
                }

                repo_info = requests.get(repo_endpoint, headers=headers)
                repo_info_json = repo_info.json()
                repo_id = repo_info_json["id"]

                endpoint = f"https://api.github.com/repositories/{repo_id}/environments/{env_name}/secrets/{secret_name}"
                response = requests.put(endpoint, json=secret_data, headers=headers)

                if (response.status_code == 200 or response.status_code == 201):
                    print(f"Environment Secret '{secret_name}' created successfully.")
                else:
                    print(f"Error creating Environment Secret '{secret_name}'. Status code: {response.status_code}")
                    print(response.text)
        else:
            print(f"Repository {repo_name} already exists!")

make_api_call('.github/example-files/repo-example.json', "my-org-alex", "https://api.github.com/orgs/my-org-alex/repos")