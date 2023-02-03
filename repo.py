from github import Repository

class Repo:
    # mapping of all Repositories to their Repo objects
    def __init__(self, repo_info: Repository):
        self.name = repo_info.name
        self.repo_full_name = repo_info.full_name
        self.num_stars = repo_info.stargazers_count
        self.archived = repo_info.archived
        self.created_at = repo_info.created_at
        self.description = repo_info.description
        self.fork = repo_info.fork
        self.forks_count = repo_info.forks_count
        self.language = repo_info.language
        self.mirror_url = repo_info.mirror_url
        self.open_issues_count = repo_info.open_issues_count
        self.ssh_url = repo_info.ssh_url
        self.html_url = repo_info.html_url
        self.updated_at = repo_info.updated_at
        self.watchers_count = repo_info.watchers_count
        self.default_branch = repo_info.default_branch
        self.id = repo_info.id

        #self.num_stars = repo_info.Repository.
        #self.has_dependabot_commits = has_dependabot_commits
        #self.has_renovate_config = has_renovate_config
        #self.has_renovate_commits = has_renovate_commits
        #self.last_commit_date = last_commit_date


    #def __repr__(self):
    #    return f"Repo({self.repo_full_name}, {self.num_stars}, {self.has_dependabot_file}, {self.has_dependabot_commits}, {self.has_renovate_config}, {self.has_renovate_commits}, {self.last_commit_date})"

    #def __str__(self):
    #    return f"Repo({self.repo_full_name}, {self.num_stars}, {self.has_dependabot_file}, {self.has_dependabot_commits}, {self.has_renovate_config}, {self.has_renovate_commits}, {self.last_commit_date})"
