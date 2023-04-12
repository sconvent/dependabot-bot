class Config:
    def __init__(self, input_config):
        self.username = "username" in input_config and input_config["username"] or "project-maintenance-bot"
        self.branch_name = "branch_name" in input_config and input_config["branch_name"] or "add-dependabot"
        self.ignored_repos = "ignored_repos" in input_config and input_config["ignored_repos"] or []
