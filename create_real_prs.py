import time

def create_real_prs(github_client, repos, dry_run):
    for repo in repos.values():
        try:
            if not repo.has_advanced_info:
                print(f"Skipping {repo.full_name} because it has no advanced info")
                continue

            if repo.has_dependabot_config or repo.has_renovate_config:
                print(f"Skipping {repo.full_name} because it already has dependabot or renovate config")
                continue

            # Make sure fork  exists
            try:
                potentially_existing_fork = github_client.get_repo(f"project-maintenance-bot/{repo.name}")
            except:
                print("Fork does not exist")
                continue

            # Get fork
            fork = github_client.get_repo(f"project-maintenance-bot/{repo.name}")
            # Search for PRs from the bot
            fork.open_prs = fork.get_pulls(state='open', sort='created', direction='desc')
            # Get comments from PRs
            for pr in fork.open_prs:
                if pr.user.login == "project-maintenance-bot":
                    pr.comments = pr.get_issue_comments()
                    for comment in pr.comments:
                        if comment.user.login == "sconvent" and "LGTM" in comment.body:
                            print(f"Creating real PR for {repo.full_name}")
                            create_pr(github_client, repo, fork, comment, dry_run)
                            break
            # wait 60 seconds
            time.sleep(60)
        except Exception as e:
            print(f"Error while processing {repo.full_name}: {e}")

def create_pr(github_client, repo, fork, comment, dry_run):
    if not dry_run:
        # Get repo
        github_repo = github_client.get_repo(repo.full_name)
        # Create PR
        github_repo.create_pull(
            title="Add Dependabot config",
            body=comment.body,
            head=f"project-maintenance-bot:add-dependabot",
            base=repo.default_branch,
    )
