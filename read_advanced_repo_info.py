from github import Github

def read_advanced_repo_info(github_client: Github, repos):
    for repo in repos.values():
        if not repo.has_advanced_info:
            print(f"Reading advanced info for repo {repo.full_name}")
            repo_info = github_client.get_repo(repo.full_name)

            repo.languages = repo_info.get_languages()
            #repo_info.get_pulls
            
            repo.has_advanced_info = True
        else:
            print(f"Advanced info for repo {repo.full_name} already read")
