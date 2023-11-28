import json

json_file = '.github/example-files/repo-example.json'

with open(json_file, 'r') as file:
    data = json.load(file)

for repo in data["repositories"]:
    print(f"Repository: {repo['repo_name']}")
    
    print("Environments:")
    for env in repo["environments"]:
        print(f"  {env['env_name']}, Production: {env['production']}")

    print("Repository Variables:")
    for var in repo["repo_variables"]:
        print(f"  {var['repo_var_name']}: {var['value']}")

    print("Repository Secrets:")
    for secret in repo["repo_secrets"]:
        print(f"  {secret['repo_secret_name']}: {secret['value']}")

    print("\n")