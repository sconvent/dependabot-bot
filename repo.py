class Repo:
    def __init__(self, repo_full_name, num_stars, has_dependabot_file, has_dependabot_commits, has_renovate_config, has_renovate_commits, last_commit_date):
        self.repo_full_name = repo_full_name
        self.num_stars = num_stars
        self.has_dependabot_file = has_dependabot_file
        self.has_dependabot_commits = has_dependabot_commits
        self.has_renovate_config = has_renovate_config
        self.has_renovate_commits = has_renovate_commits
        self.last_commit_date = last_commit_date

    def __repr__(self):
        return f"Repo({self.repo_full_name}, {self.num_stars}, {self.has_dependabot_file}, {self.has_dependabot_commits}, {self.has_renovate_config}, {self.has_renovate_commits}, {self.last_commit_date})"

    def __str__(self):
        return f"Repo({self.repo_full_name}, {self.num_stars}, {self.has_dependabot_file}, {self.has_dependabot_commits}, {self.has_renovate_config}, {self.has_renovate_commits}, {self.last_commit_date})"
