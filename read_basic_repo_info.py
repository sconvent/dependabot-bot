from repo import Repo

def read_basic_repo_info(github_client, repos):
    query = "stars:>1000"
    sort = "stars"
    result = github_client.search_repositories(query=query, sort=sort, order='desc')

    max_count = 10
    count = 0
    for repo in result:
        if count == max_count:
            break
        repos[repo.full_name] = Repo(repo_info = repo)
        count += 1
