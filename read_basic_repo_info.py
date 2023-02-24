from repo import Repo

def read_basic_repo_info(github_client, repos, max_count):
    last_num_stars = 1000000
    finished = False
    count = 0
    while not finished and len(repos.keys()) < max_count:
        finished = True

        query = f"stars:1000..{last_num_stars+1}"
        sort = "stars"
        result = github_client.search_repositories(query=query, sort=sort, order='desc')

        for repo in result:
            if len(repos.keys()) >= max_count:
                break
            if repo.full_name not in repos:
                repos[repo.full_name] = Repo(repo_info = repo)
                print(f"{count}: Added repo {repo.full_name} to db")
            else:
                print(f"{count}: Repo {repo.full_name} already in db")
            last_num_stars = repo.stargazers_count
            count += 1
            finished = False
