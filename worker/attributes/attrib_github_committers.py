import os
import requests

ATTRIBUTE_SLUG = 'repo_commiters'
WEIGHT = 10


def run(project):
    """ Look to see if a project has a readme file """
    repo_url = project.get('repo_url', None)
    if not repo_url:
        return None

    repo_url = repo_url.replace("github.com/", "api.github.com/repos/")

    r = requests.get("{0}/contributors".format(repo_url))
    if r and r.status_code == 200:
        value = len(r.json())
    else:
        return None

    return {'name': ATTRIBUTE_SLUG, 'value': value}


def score(project):
    return