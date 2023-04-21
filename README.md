![CI](https://github.com/sconvent/dependabot-bot/actions/workflows/ci.yml/badge.svg?branch=main)

# Project Maintenance Bot
**Work in Progress**

A set of scripts to automatically establish some basic code maintenance and quality assurance measures.
Currently the only offered functionality is to create PRs which add a Dependabot config to open source projects.

For the future it is planned to add the functionality to create basic CI pipelines and to scan and fix problems found by static code analysis.

## Install Dependencies
Install required dependencies with `pip install -r requirements.txt`

## Usage

### Token
A Github Personal Access Token is needed for some steps. It needs read access to the target repos as well as the right to create forks and PRs.

Store the token in the environment variable `GITHUB_TOKEN`

## Config
A config.json file of the following format must be placed in the root folder:
```
{
    "ignored_repos": [],
    "user_name": "<user_name>",
    "branch_name": "<branch_name>",
    "approving_user": "<approving_user>"
}
```

## Steps

- Scan for repositories (sorted by number of stars) with: `python3 main.py read_basic_repo_info <max_count>`
- Read out advanced info for each scanned repository: `python3 main.py read_advanced_repo_info`
- Create Forks and PRs (in the forks): `python3 main.py create_forks_and_prs`
- Scan these PRs for approval and open PR on the target repository: `python3 main.py create_real_prs`
