from github import Github
import time

def read_advanced_repo_info(github_client: Github, repos):
    for repo in repos.values():
        if repo.has_advanced_info:
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

            # TODO: Add the following package managers:
            # bundler
            # cargo
            # composer
            # docker
            # mix
            # elm
            # git submodules
            # github actions (/.github/workflows/*.yaml)
            # gomod
            # nuget
            # pub
            # terraform

            # TODO: Get info whether repo already has Dependabot config
            # TODO: Get info whether Dependabot has opened PRs
            #repo_info.get_pulls
            # TODO: Get info whether repo has Renovate config
            # TODO: Get info on activity of repo
            
            repo.has_advanced_info = True
        else:
            print(f"Advanced info for repo {repo.full_name} already read")
        

def find_files(github_client, repo, languages, filename):
    # Check if repo uses any of the given languages
    languages_intersection = [language for language in languages if language in repo.languages]
    if len(languages_intersection) > 0: 
        # search for filename
        result = github_client.search_code(query=f"repo:{repo.full_name} filename:{filename}")
        relevant_files = []
        for file in result:
            if file.path == filename or file.path.endswith("/"+filename):
                print(f"Found filename for repo {repo.full_name} at /{file.path}")
                relevant_files.append("/"+file.path)
            # To avoid rate limit
            time.sleep(0.1)
        # To avoid rate limit
        time.sleep(1)
        return relevant_files
    else:
        return []
