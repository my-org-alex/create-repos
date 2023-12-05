# create-repos
This repository has the goal of creating other repositories in an automated fashion.
It has a Workflow that will run a python script which will recieve a JSON file as an input with all the repository info (can have multiple repositories).

The script makes multiple API Calls for the creation of the resources, this means you MUST provide your GitHub Personal Token

The script can create one or more repositories with one or more:
    - Repository Environments;
    - Environment Secrets;
    - Repository Variables;
    - Repository Secrets.
Other resources, must be implemented manually (for now)

Check "repo-example.json" for guidance on the JSON file structure.