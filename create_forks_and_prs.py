import time

def create_forks_and_prs(github_client, repos):
    for repo in repos.values():
        
        # Check if fork already exists
        try:
            potentially_existing_fork = github_client.get_repo(f"sconvent/{repo.name}")
            print("Fork already exists")
            return
        except:
            pass

        # If not, create fork
        print(f"Creating fork for {repo.full_name}")
        github_repo = github_client.get_repo(repo.full_name)
        github_repo.create_fork()

        # Get fork
        fork = github_client.get_repo(f"sconvent/{repo.name}")

        # Create branch
        print(f"Creating branch for {repo.full_name}")
        fork.create_git_ref(ref=f"refs/heads/add-dependabot", sha=repo.sha)

        # Create dependabot.yml
        print(f"Creating dependabot.yml for {repo.full_name}")
        fork.create_file(path="dependabot.yml", message="Add dependabot.yml", content="TBD", branch="add-dependabot")

        # Create pull request
        # Not yet implemented

        # Wait 60 seconds
        time.sleep(60)
