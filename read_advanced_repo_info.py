from github import Github
import time

def read_advanced_repo_info(github_client: Github, repos):
    for repo in repos.values():
        if not repo.has_advanced_info:
            print(f"Reading advanced info for repo {repo.full_name}")
            repo_info = github_client.get_repo(repo.full_name)

            repo.languages = repo_info.get_languages()

            # package.json (npm, yarn)
            # TODO: Match more languages
            repo.package_json_files = find_files(github_client, repo, ["JavaScript", "TypeScript"], "package.json")
            
            # pom.xml (maven)
            repo.pom_xml_files = find_files(github_client, repo, ["Java", "Kotlin", "Scala"], "pom.xml")

            # build.gradle (gradle)
            repo.build_gradle_files = find_files(github_client, repo, ["Java", "Kotlin", "Scala"], "build.gradle")

            # requirements.txt (pip)
            repo.requirements_txt_files = find_files(github_client, repo, ["Python"], "requirements.txt")

            # Gemfile (bundler)
            repo.gemfile_files = find_files(github_client, repo, ["Ruby"], "Gemfile")

            # Cargo.toml (cargo)
            repo.cargo_toml_files = find_files(github_client, repo, ["Rust"], "Cargo.toml")

            # composer.json (composer)
            repo.composer_json_files = find_files(github_client, repo, ["PHP"], "composer.json")

            # Dockerfile (docker)
            repo.dockerfile_files = find_files(github_client, repo, ["Dockerfile"], "Dockerfile")

            # mix.exs (mix)
            repo.mix_exs_files = find_files(github_client, repo, ["Elixir"], "mix.exs")

            # elm.json (elm)
            repo.elm_json_files = find_files(github_client, repo, ["Elm"], "elm.json")

            # .gitmodules (git submodules)
            # TODO: Match all languages
            repo.gitmodules_files = find_files(github_client, repo, [""], ".gitmodules")

            # .github/workflows/*.yaml (github actions)
            # TODO: Match all languages
            repo.github_workflows_files = find_files(github_client, repo, [""], ".github/workflows")

            # go.mod (gomod)
            repo.go_mod_files = find_files(github_client, repo, ["Go"], "go.mod")

            # *.csproj (nuget)
            # TODO: Potentially match more languages
            # TODO: Check whether this is the correct filename
            # TODO: Match with regex
            repo.csproj_files = find_files(github_client, repo, ["C#"], "*.csproj")

            # pubspec.yaml (pub)
            repo.pubspec_yaml_files = find_files(github_client, repo, ["Dart"], "pubspec.yaml")

            # *.tf (terraform)
            # TODO: Match with regex
            repo.tf_files = find_files(github_client, repo, ["Terraform"], "*.tf")

            # Get info whether repo already has Dependabot config
            repo.dependabot_config_files = find_files(github_client, repo, [""], ".github/dependabot.yml")
            repo.has_dependabot_config = len(repo.dependabot_config_files) > 0

            # TODO: Get info whether Dependabot has opened PRs
            #repo_info.get_pulls

            # Get info whether repo has Renovate config
            repo.renovate_config_files = find_files(github_client, repo, [""], ".github/renovate.json")
            repo.has_renovate_config = len(repo.renovate_config_files) > 0

            # Get info on activity of repo
            repo.activity = repo_info.get_stats_participation().all
            
            repo.has_advanced_info = True
        else:
            print(f"Advanced info for repo {repo.full_name} already read")
        

# TODO: Match with regex
def find_files(github_client, repo, languages, filename):
    # Check if repo uses any of the given languages
    languages_intersection = [language for language in languages if language in repo.languages]
    if len(languages_intersection) > 0: 
        # search for filename
        result = github_client.search_code(query=f"repo:{repo.full_name} filename:{filename}")
        relevant_files = []
        count = 0
        for file in result:
            if file.path == filename or file.path.endswith("/"+filename):
                print(f"Found filename for repo {repo.full_name} at /{file.path}")
                relevant_files.append("/"+file.path)
            count += 1
            if count > 50:
                # No more than 50 results
                break
            # To avoid rate limit
            time.sleep(2)
        return relevant_files
    else:
        return []
