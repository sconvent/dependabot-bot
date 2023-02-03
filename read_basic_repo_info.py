from repo import Repo

def read_basic_repo_info(github_client, repos, max_count):
    query = "stars:>1000"
    sort = "stars"
    result = github_client.search_repositories(query=query, sort=sort, order='desc')

    count = 0
    for repo in result:
        if count == max_count:
            break
        if repo.full_name not in repos:
            repos[repo.full_name] = Repo(repo_info = repo)
            print(f"{count}: Added repo {repo.full_name} to db")
        else:
            print(f"{count}: Repo {repo.full_name} already in db")
        count += 1
