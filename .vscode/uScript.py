import os
import requests
from git import Repo

# GitHub credentials
github_username = "DrQuackster"
github_token = "your-token"

# GitHub repository information
repo_owner = "DrQuackster"
repo_name = "uList"

# List of uBO filter lists to merge
filter_lists = [
    "https://gitlab.com/hagezi/mirror/-/raw/main/dns-blocklists/adblock/ultimate.txt",
    "https://raw.githubusercontent.com/iam-py-test/uBlock-combo/main/list.txt",
    "https://raw.githubusercontent.com/iam-py-test/uBlock-combo/main/list.txt",
    # Add more filter lists as needed
]

# Clone the uList repository
repo_url = f"https://github.com/{repo_owner}/{repo_name}.git"
local_repo_path = f"./{repo_name}"

# Clone the repository if it doesn't exist, otherwise pull the latest changes
if not os.path.exists(local_repo_path):
    Repo.clone_from(repo_url, local_repo_path)
else:
    repo = Repo(local_repo_path)
    origin = repo.remote(name='origin')
    origin.pull()

# Fetch and merge filter lists
merged_content = ""
for filter_list_url in filter_lists:
    response = requests.get(filter_list_url)
    if response.status_code == 200:
        merged_content += f"\n\n# {filter_list_url}\n\n" + response.text

# Write merged content to the uList file
ulist_file_path = os.path.join(local_repo_path, "uList.txt")
with open(ulist_file_path, "a") as ulist_file:
    ulist_file.write(merged_content)

# Stage and commit changes using Git command line
os.system(f'git -C "{local_repo_path}" add uList.txt')
os.system(f'git -C "{local_repo_path}" commit -m "Merge uBO filter lists"')

# Push changes to GitHub using Git command line
os.system(f'git -C "{local_repo_path}" push origin master')

print("Filter lists merged and committed successfully.")
