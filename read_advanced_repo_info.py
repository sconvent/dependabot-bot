from github import Github
import os
import pathlib
import shutil
import pickle
import re


def read_advanced_repo_info(github_client: Github, config, repos):
    # potentially delete folder
    try:
        shutil.rmtree("repos")
    except:
        pass

    # create folder
    os.mkdir("repos")

    count = 0
    for repo in repos.values():
        try:
            if not repo.has_advanced_info and repo.full_name not in config.ignored_repos:
                # save local_db every 50 repos
                count += 1
                if count % 50 == 0:
                    # save local_db
                    with(open('local_db', 'wb')) as f:
                        pickle.dump(repos, f)


                # Check if folder exists
                folder_path = f"repos/{repo.full_name.replace('/', '_')}"
                if os.path.isdir(folder_path):
                    print(f"Repo {repo.full_name} already cloned. Will pull instead.")
                    command = f"cd {folder_path} && git pull"
                    os.system(command)
                else:
                    print(f"Cloning repo {repo.full_name}")

                    folder_path = f"repos/{repo.full_name.replace('/', '_')}"
                    command = f"git clone --depth 1 https://github.com/{repo.full_name}.git {folder_path}"
                    os.system(command)

                print(f"Reading advanced info for repo {repo.full_name}")
                repo_info = github_client.get_repo(repo.full_name)

                repo.languages = repo_info.get_languages()

                # Todo: for all ecosystems, check if the respective file actually contains dependencies

                # package.json (npm, yarn)
                # TODO: Match more languages
                repo.package_json_files = find_files(repo, ["JavaScript", "TypeScript"], "package.json")
                repo.package_json_files = filter_files(repo.package_json_files, r".*[dD]ependencies.*")

                # pom.xml (maven)
                repo.pom_xml_files = find_files(repo, ["Java", "Kotlin", "Scala"], "pom.xml")
                repo.pom_xml_files = filter_files(repo.pom_xml_files, r".*dependencies.*")

                # build.gradle (gradle)
                repo.build_gradle_files = find_files(repo, ["Java", "Kotlin", "Scala"], "build.gradle")
                repo.build_gradle_files = filter_files(repo.build_gradle_files, r".*dependencies.*")

                # requirements.txt (pip)
                repo.requirements_txt_files = find_files(repo, ["Python"], "requirements.txt")
                # requirements.txt only contains dependencies so no need to filter

                # Gemfile (bundler)
                repo.gemfile_files = find_files(repo, ["Ruby"], "Gemfile")
                # No easy way to filter Gemfiles

                # Cargo.toml (cargo)
                repo.cargo_toml_files = find_files(repo, ["Rust"], "Cargo.toml")
                repo.cargo_toml_files = filter_files(repo.cargo_toml_files, r".*dependencies.*")

                # composer.json (composer)
                repo.composer_json_files = find_files(repo, ["PHP"], "composer.json")
                repo.composer_json_files = filter_files(repo.composer_json_files, r".*require.*")
                
                # Dockerfile (docker)
                repo.dockerfile_files = find_files(repo, ["Dockerfile"], "Dockerfile")

                # mix.exs (mix)
                repo.mix_exs_files = find_files(repo, ["Elixir"], "mix.exs")
                repo.mix_exs_files = filter_files(repo.mix_exs_files, r".*def deps do.*")            

                # Todo: Filter further files for dependencies
                # elm.json (elm)
                repo.elm_json_files = find_files(repo, ["Elm"], "elm.json")

                # .gitmodules (git submodules)
                # matches all languages
                repo.gitmodules_files = find_files(repo, ["*"], ".gitmodules")

                # .github/workflows/*.yaml (github actions)
                # matches all languages
                repo.github_workflows_files = find_files(repo, ["*"], ".github/workflows")

                # go.mod (gomod)
                repo.go_mod_files = find_files(repo, ["Go"], "go.mod")

                # *.csproj (nuget)
                # TODO: Potentially match more languages
                # TODO: Check whether this is the correct filename
                # TODO: Match with regex
                repo.csproj_files = find_files(repo, ["C#"], "*.csproj")

                # pubspec.yaml (pub)
                repo.pubspec_yaml_files = find_files(repo, ["Dart"], "pubspec.yaml")

                # *.tf (terraform)
                # TODO: Match with regex
                repo.tf_files = find_files(repo, ["Terraform"], "*.tf")

                # Get info whether repo already has Dependabot config
                repo.dependabot_config_files = find_files(repo, ["*"], ".github/dependabot.yml")
                repo.has_dependabot_config = len(repo.dependabot_config_files) > 0

                # TODO: Get info whether Dependabot has opened PRs
                #repo_info.get_pulls

                # Get info whether repo has Renovate config
                repo.renovate_config_files = find_files(repo, ["*"], "./renovate.json")
                repo.has_renovate_config = len(repo.renovate_config_files) > 0

                # Get info on activity of repo
                repo.activity = repo_info.get_stats_participation().all
                
                repo.has_advanced_info = True

                # Delete folder
                shutil.rmtree(folder_path)
            else:
                print(f"Advanced info for repo {repo.full_name} already read, no relevant languages found or repo ignored.")  
        except Exception as e:
            print(f"Error while reading advanced info for repo {repo.full_name}: {e}")      

def find_files(repo, languages, filename):
    # Check if repo uses any of the given languages
    languages_intersection = [language for language in languages if language in repo.languages]
    if len(languages_intersection) > 0 or languages == ["*"]: 
        # use pathlib to search directory for filename
        folder_path = f"repos/{repo.full_name.replace('/', '_')}"
        results = pathlib.Path(folder_path).glob(f"**/{filename}")
        results = [str(result) for result in results]
        print(f"Found {languages_intersection} files for repo {repo.full_name} at {results}")
        return results
    else:
        return []

# Filter files that match a certain regex
def filter_files(files, regex):
    result = []
    for file in files:
        s = ""
        # get file content
        with open(file) as f: s = f.read()
        # check if file content matches regex
        if re.search(regex, s): result.append(file)
        else: print(f"File {file} does not match regex {regex}")
    return result
