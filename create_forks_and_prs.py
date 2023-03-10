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
    open-pull-requests-limit: 10
    schedule:
        interval: "weekly"
    # Ignore major version upgrades
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]

{{/configs}}
        """,
        {'configs': configs},
    ).strip()+"\n"

def render_pr_message():
    return pystache.render(
        """
This PR adds a Dependabot configuration to this repository.
Dependabot will automatically create PRs to update your dependencies.
It's a good way to keep your dependencies up to date and to make sure that you are always using the latest version of your dependencies.

Some more thoughts:
This configuration will ignore major version upgrades. This is because major version upgrades often require manual work to make sure that the upgrade works as expected.
This PR was created by the [Project Maintenance Bot](github.com/project-maintenance-bot), a bot that helps with the maintenance of open-source projects.
        """,
        {})

def create_configs(files, ecosystem):
    configs = [{'ecosystem': ecosystem, 'directory': extract_path(path)} for path in files]
    # sort by least nested directory and then by length
    configs.sort(key=lambda x: (x['directory'].count('/'), len(x['directory'])))
    # maximum number of configs is 3
    configs = configs[:3]
    return configs

def create_forks_and_prs(github_client, repos, dry_run):
    for repo in repos.values():
        if not repo.has_advanced_info:
            print(f"Skipping {repo.full_name} because it has no advanced info")
            continue

        if repo.has_dependabot_config or repo.has_renovate_config:
            print(f"Skipping {repo.full_name} because it already has dependabot or renovate config")
            continue

        if not dry_run:
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

            # Todo: Check if branch already exists
            # Create branch
            print(f"Creating branch for {repo.full_name}")
            fork.create_git_ref(ref=f"refs/heads/add-dependabot", sha=sha)

        # Create dependabot.yml
        configs = \
        create_configs(repo.package_json_files, 'npm') \
        + create_configs(repo.pom_xml_files, 'maven') \
        + create_configs(repo.build_gradle_files, 'gradle') \
        + create_configs(repo.requirements_txt_files, 'pip') \
        + create_configs(repo.gemfile_files, 'bundler') \
        + create_configs(repo.cargo_toml_files, 'cargo') \
        + create_configs(repo.composer_json_files, 'composer') \
        + create_configs(repo.csproj_files, 'nuget') \
        + create_configs(repo.dockerfile_files, 'docker') \
        + create_configs(repo.gitmodules_files, 'submodules') \
        + create_configs(repo.mix_exs_files, 'elixir') \
        + create_configs(repo.go_mod_files, 'go') \
        + create_configs(repo.tf_files, 'terraform') \
        + create_configs(repo.elm_json_files, 'elm')

        # Abort if there are no configs
        if len(configs) == 0:
            print(f"Skipping {repo.full_name} because there are no configs")
            continue

        content = render_dependabot_config(configs)
        if dry_run:
            print("CONTENT:")
            print(content)
            print("END CONTENT")
        
        if not dry_run:
            # Todo: Check if file already exists
            fork.create_file(path="dependabot.yml", message="Add dependabot.yml", content=content, branch="add-dependabot")

            # Create pull request if not exists
            # Not yet implemented

            # Wait 60 seconds
            time.sleep(60)
