import time

def create_forks_and_prs(github_client, repos):
    for repo in repos.values():
        
        # Check if fork already exists
        try:
            potentially_existing_fork = github_client.get_repo(f"sconvnet/{repo.name}")
            print("Fork already exists")
            return
        except:
            pass

        # If not, create fork
        print(f"Creating fork for {repo.full_name}")
        github_repo = github_client.get_repo(repo.full_name)
        github_repo.create_fork()

        # Wait 60 seconds
        time.sleep(60)
