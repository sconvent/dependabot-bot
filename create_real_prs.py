import time

def create_real_prs(github_client, config, repos, dry_run):
    for repo in repos.values():
        try:
            if repo.full_name in config.ignored_repos:
                print(f"Skipping {repo.full_name} because it is in the ignore list")
                continue
            
            if not repo.has_advanced_info:
                print(f"Skipping {repo.full_name} because it has no advanced info")
                continue

            if repo.has_dependabot_config or repo.has_renovate_config:
                print(f"Skipping {repo.full_name} because it already has dependabot or renovate config")
                continue

            if repo.created_real_pr:
                print(f"Skipping {repo.full_name} because it already has a real PR")
                continue

            # safety net: only create pr if no previous pr exists
            original_repo = github_client.get_repo(repo.full_name)
            # get all open and closed prs by the user project-maintenance-bot
            closed_prs = original_repo.get_pulls(state='closed', head='project-maintenance-bot:add-dependabot')
            open_prs = original_repo.get_pulls(state='open', head='project-maintenance-bot:add-dependabot')
            # if there are any open or closed prs, skip
            if closed_prs.totalCount > 0 or open_prs.totalCount > 0:
                print(f"Skipping {repo.full_name} because it already has a PR")
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
            fork.open_prs = fork.get_pulls(state='open', sort='created')
            print(f"Found PR for {repo.full_name}")
            # Get comments from PRs
            for pr in fork.open_prs:
                if pr.user.login == "project-maintenance-bot":
                    comments = pr.get_issue_comments()
                    for comment in comments:
                        if comment.user.login == "sconvent" and comment.body == "LGTM":
                            print(f"Creating real PR for {repo.full_name}")
                            create_pr(github_client, repo, fork, pr.body, dry_run)
                            # wait 60 seconds
                            time.sleep(60)
                            break
                    print(f"No approving comment in PR for {repo.full_name}")
                    time.sleep(5)
                            
        except Exception as e:
            print(f"Error while processing {repo.full_name}: {e}")
            time.sleep(5)

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
        print(f"Created real PR for {repo.full_name}")
        repo.created_real_pr = True
    else:
        print(f"Would have created real PR for {repo.full_name}")
