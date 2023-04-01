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
This PR adds a [Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/managing-pull-requests-for-dependency-updates) configuration to this repository.
Dependabot will automatically create PRs to upgrade dependencies.
It's a good way to keep your dependencies up to date and to make sure that you are always using the latest version of your dependencies.

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
        try:
            if not repo.has_advanced_info:
                print(f"Skipping {repo.full_name} because it has no advanced info")
                continue

            if repo.has_dependabot_config or repo.has_renovate_config:
                print(f"Skipping {repo.full_name} because it already has dependabot or renovate config")
                continue

            # Skip if project had less than 20 commits in the last year
            if sum(repo.activity) < 20:
                print(f"Skipping {repo.full_name} because it had less than 20 commits in the last year")
                continue

            # Gather configs
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

            # Sort by length of directory
            configs.sort(key=lambda x: len(x['directory']))

            # Abort if there are no configs
            if len(configs) == 0:
                print(f"Skipping {repo.full_name} because there are no configs")
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
                    print("Waiting 30 seconds for fork to be created")
                    time.sleep(30)

                # Get fork
                fork = github_client.get_repo(f"project-maintenance-bot/{repo.name}")
                # Get default branch
                print(fork.default_branch)
                try:
                    branch = fork.get_git_ref("heads/add-dependabot")
                    print("Deleting already existing branch")
                    branch.delete()
                    print("Deleted already existing branch")
                except:
                    print("Branch does not exist yet")
                    pass
                time.sleep(5)
                sha = fork.get_branch(fork.default_branch).commit.sha

                # Create branch
                print(f"Creating branch for {repo.full_name}")
                fork.create_git_ref(ref=f"refs/heads/add-dependabot", sha=sha)
                time.sleep(5)

            # Create dependabot.yml
            content = render_dependabot_config(configs)
            if dry_run:
                print("CONTENT:")
                print(content)
                print("END CONTENT")
            
            if not dry_run:
                print(f"Creating dependabot.yml for {repo.full_name} on branch add-dependabot")
                fork.create_file(path=".github/dependabot.yml", message="Add dependabot.yml", content=content, branch="add-dependabot")
                time.sleep(3)

                # Create pull request if not exists
                if len(list(fork.get_pulls(state='open', head='project-maintenance-bot:add-dependabot'))) == 0:
                    print(f"Creating pull request for {repo.full_name}")
                    fork.create_pull(title="Add dependabot.yml", body=render_pr_message(), head="add-dependabot", base=fork.default_branch)
                    time.sleep(5)
                else:
                    print(f"Pull request already exists for {repo.full_name}")
                
                # Wait 50 seconds
                print("Waiting 50 seconds")
                time.sleep(50)
        except Exception as e:
            print(f"Error while processing {repo.full_name}: {e}")
