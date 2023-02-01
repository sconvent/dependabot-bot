import pprint
import pickle
import os
from repo import Repo
from github import Github

# load local_db
repos = []
try:
    with(open('local_db', 'rb')) as f:
        repos = pickle.load(f)
except:
    repos = []

stars = 1000

# read env var for github token
token = os.getenv('GITHUB_TOKEN')

g = Github(token)
result = g.search_repositories(query=f"stars:>{stars}", sort='stars', order='desc')
count = 0
for repo in result:
    repos.append(Repo(repo_full_name = repo.full_name,
                      num_stars = repo.stargazers_count,
                      has_dependabot_file = False,
                      has_dependabot_commits = False,
                      has_renovate_config = False,
                      has_renovate_commits = False,
                      last_commit_date = 0))
    count += 1
    if count == 100:
        break

pprint.pprint(repos)

# save local_db
with(open('local_db', 'wb')) as f:
    pickle.dump(repos, f)
