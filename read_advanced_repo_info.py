from github import Github
import time

def read_advanced_repo_info(github_client: Github, repos):
    for repo in repos.values():
        if repo.has_advanced_info:
            print(f"Reading advanced info for repo {repo.full_name}")
            repo_info = github_client.get_repo(repo.full_name)

            repo.languages = repo_info.get_languages()

            # package.json
            if "JavaScript" in repo.languages or "TypeScript" in repo.languages: 
                # search for package.json
                result = github_client.search_code(query=f"repo:{repo.full_name} filename:package.json")
                relevant_files = []
                for file in result:
                    if file.path.endswith("/package.json"):
                        print(f"Found package.json for repo {repo.full_name} at /{file.path}")
                        relevant_files.append("/"+file.path)
                repo.package_json_files = relevant_files

            #repo_info.get_pulls
            
            repo.has_advanced_info = True
        else:
            print(f"Advanced info for repo {repo.full_name} already read")
        
        # To avoid rate limit
        time.sleep(5)
