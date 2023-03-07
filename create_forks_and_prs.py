import time
import pystache

def extract_path(full_path):
    return "/"+"/".join(full_path.split("/")[2:-1])


def render_dependabot_config(configs):
    return pystache.render(
        """
version: 2
updates:
{{#configs}}
  - package-ecosystem: "{{ecosystem}}"
    directory: "{{directory}}"
    schedule:
      interval: "weekly"

{{/configs}}
        """,
        {'configs': configs},
    )

def create_forks_and_prs(github_client, repos):
    # Todo: Implement dry run

    for repo in repos.values():
        
        # Check if fork already exists
        try:
            potentially_existing_fork = github_client.get_repo(f"project-maintenance-bot/{repo.name}")
            print("Fork already exists")
        except:
            # If not, create fork
            print(f"Creating fork for {repo.full_name}")
            github_repo = github_client.get_repo(repo.full_name)
            github_repo.create_fork()
            time.sleep(30)

        # Get fork
        fork = github_client.get_repo(f"project-maintenance-bot/{repo.name}")
        # Get default branch
        print(fork.default_branch)
        sha = fork.get_branch(fork.default_branch).commit.sha

        # Create branch
        print(f"Creating branch for {repo.full_name}")
        fork.create_git_ref(ref=f"refs/heads/add-dependabot", sha=sha)

        # Create dependabot.yml
        print(f"Creating dependabot.yml for {repo.full_name}")
        # Todo: Add more ecosystems
        configs = \
        [{'ecosystem': 'maven', 'directory': extract_path(path)} for path in repo.pom_xml_files] \
        + [{'ecosystem': 'gradle', 'directory': extract_path(path)} for path in repo.build_gradle_files] \
        + [{'ecosystem': 'npm', 'directory': extract_path(path)} for path in repo.package_json_files]
        content = render_dependabot_config(configs)
        #print("CONTENT:")
        #print(content)
        #print("END CONTENT")
        fork.create_file(path="dependabot.yml", message="Add dependabot.yml", content=content, branch="add-dependabot")

        # Create pull request
        # Not yet implemented

        # Wait 60 seconds
        time.sleep(30)
