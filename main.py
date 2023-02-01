import pprint
import pickle
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

g = Github()
result = g.search_repositories(query=f"stars:>{stars}", sort='stars', order='desc')
count = 0
for repo in result:
    print(repo.stargazers_count, repo.html_url)
    repos.append(Repo(repo_link = repo.html_url,
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
