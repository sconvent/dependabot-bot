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

# read env var for github token
token = os.getenv('GITHUB_TOKEN')

# create github client
if token is None:
    github_client = Github()
else:
    github_client = Github(token)

arguments = sys.argv
match arguments[1]:
    # Read basic repo info for relevant repos
    case "read_basic_repo_info":
        max_count = arguments[2]
        read_basic_repo_info(github_client, repos, max_count)
    case "read_advanced_info":
        read_advanced_repo_info(github_client, repos)
    case "create_forks_and_prs":
        create_forks_and_prs(github_client, repos)
    case "create_real_prs":
        create_real_prs(github_client, repos)
    case "dump_db":
        dump_db(github_client, repos)
    case _:
        print("Invalid argument")

# save local_db
with(open('local_db', 'wb')) as f:
    pickle.dump(repos, f)
