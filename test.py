from github import Github

# create github client
github_client = Github(per_page=100)

# get repo
repo = github_client.get_repo("grammyjs/grammY")

# get all open and closed prs by the user project-maintenance-bot
closed_prs = repo.get_pulls(state='closed', head='project-maintenance-bot:add-dependabot')
closed_prs.totalCount
open_prs = repo.get_pulls(state='open', head='project-maintenance-bot:add-dependabot')
# print size of prs
print(f"Closed PRs: {closed_prs.totalCount}")
print(f"Open PRs: {open_prs.totalCount}")
