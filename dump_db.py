import jsons

def dump_db(github_client, repos):
    with open('db_dump.json', 'w') as outfile:
        outfile.write(jsons.dumps(repos, strict=False, jdkwargs={"indent":4}))
