import pickle
import os
from github import Github
from read_basic_repo_info import read_basic_repo_info
from read_advanced_repo_info import read_advanced_repo_info
from create_forks_and_prs import create_forks_and_prs
from create_real_prs import create_real_prs
from dump_db import dump_db
import sys
import warnings

# ignore warnings
warnings.filterwarnings('ignore')

# load local_db
repos = dict()
try:
    with(open('local_db', 'rb')) as f:
        repos = pickle.load(f)
except:
    repos = dict()

# clean up local_db
for repo in repos.values():
    if not hasattr(repo, "created_real_pr"):
        repo.created_real_pr = False

# read env var for github token
token = os.getenv('GITHUB_TOKEN')

# create github client
if token is None:
    github_client = Github(per_page=100)
else:
    github_client = Github(per_page=100, login_or_token=token)

arguments = sys.argv
command = arguments[1]
print(f"Command: {command}")
if command == "read_basic_repo_info":
    max_count = int(arguments[2])
    read_basic_repo_info(github_client, repos, max_count)
elif command == "read_advanced_repo_info":
    read_advanced_repo_info(github_client, repos)
elif command == "create_forks_and_prs":
    create_forks_and_prs(github_client, repos, dry_run=arguments[2] == "true" if len(arguments) > 2 else False)
elif command ==  "create_real_prs":
    create_real_prs(github_client, repos, dry_run=arguments[2] == "true" if len(arguments) > 2 else False)
elif command  == "dump_db":
    dump_db(github_client, repos)
else:
    print("Invalid argument")

# save local_db
with(open('local_db', 'wb')) as f:
    pickle.dump(repos, f)
