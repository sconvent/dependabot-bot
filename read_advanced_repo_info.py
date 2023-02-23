from github import Github
import os
import pathlib
import shutil
import pickle

def read_advanced_repo_info(github_client: Github, repos):
    # potentially delete folder
    try:
        shutil.rmtree("repos")
    except:
        pass

    # create folder
    os.mkdir("repos")

    count = 0
    for repo in repos.values():
        if not repo.has_advanced_info or len(repo.languages) > 0:
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

            # package.json (npm, yarn)
            # TODO: Match more languages
            repo.package_json_files = find_files(repo, ["JavaScript", "TypeScript"], "package.json")
            
            # pom.xml (maven)
            repo.pom_xml_files = find_files(repo, ["Java", "Kotlin", "Scala"], "pom.xml")

            # build.gradle (gradle)
            repo.build_gradle_files = find_files(repo, ["Java", "Kotlin", "Scala"], "build.gradle")

            # requirements.txt (pip)
            repo.requirements_txt_files = find_files(repo, ["Python"], "requirements.txt")

            # Gemfile (bundler)
            repo.gemfile_files = find_files(repo, ["Ruby"], "Gemfile")

            # Cargo.toml (cargo)
            repo.cargo_toml_files = find_files(repo, ["Rust"], "Cargo.toml")

            # composer.json (composer)
            repo.composer_json_files = find_files(repo, ["PHP"], "composer.json")

            # Dockerfile (docker)
            repo.dockerfile_files = find_files(repo, ["Dockerfile"], "Dockerfile")

            # mix.exs (mix)
            repo.mix_exs_files = find_files(repo, ["Elixir"], "mix.exs")

            # elm.json (elm)
            repo.elm_json_files = find_files(repo, ["Elm"], "elm.json")

            # .gitmodules (git submodules)
            # TODO: Match all languages
            repo.gitmodules_files = find_files(repo, [""], ".gitmodules")

            # .github/workflows/*.yaml (github actions)
            # TODO: Match all languages
            repo.github_workflows_files = find_files(repo, [""], ".github/workflows")

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
            repo.dependabot_config_files = find_files(repo, [""], ".github/dependabot.yml")
            repo.has_dependabot_config = len(repo.dependabot_config_files) > 0

            # TODO: Get info whether Dependabot has opened PRs
            #repo_info.get_pulls

            # Get info whether repo has Renovate config
            repo.renovate_config_files = find_files(repo, [""], ".github/renovate.json")
            repo.has_renovate_config = len(repo.renovate_config_files) > 0

            # Get info on activity of repo
            repo.activity = repo_info.get_stats_participation().all
            
            repo.has_advanced_info = True
        else:
            print(f"Advanced info for repo {repo.full_name} already read or no relevant languages found")

        # Delete folder
        shutil.rmtree(folder_path)
        

def find_files(repo, languages, filename):
    # Check if repo uses any of the given languages
    languages_intersection = [language for language in languages if language in repo.languages]
    if len(languages_intersection) > 0: 
        # use pathlib to search directory for filename
        folder_path = f"repos/{repo.full_name.replace('/', '_')}"
        results = pathlib.Path(folder_path).glob(f"**/{filename}")
        results = [str(result) for result in results]
        print(f"Found {languages_intersection} files for repo {repo.full_name} at {results}")
        return results
    else:
        return []
