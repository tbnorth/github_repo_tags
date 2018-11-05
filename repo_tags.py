"""
repo_tags.py - allow GitHub repo. tagging (via proxy issues).

Terry Brown, terrynbrown@gmail.com, Mon Nov  5 16:09:19 EST 2018
"""

import json
import os
import time
from getpass import getpass
from github import Github

LOGIN_INFO_FILE = "login.info"
TAG_REPO = "repo_tags"
RATE_LIMIT = 10  # wait seconds between creating issues
URL_TEMPLATE = "https://github.com/%s/%s"

# read username / password from file or from user
if os.path.exists(LOGIN_INFO_FILE):
    USER, PWORD = open(LOGIN_INFO_FILE).read().split()
else:
    USER = input("Github username: ")
    PWORD = getpass()

GH = Github(USER, PWORD)

repos = {}
print("Reading repos")
for repo in GH.get_user().get_repos():
    # includes repos. in org.s and from other users
    org = repo.organization.login if repo.organization else repo.owner.login
    key = (repo.name, org)
    repos[key] = {'desc': repo.description, 'url': repo.url, 'org': org}

if (TAG_REPO, USER) not in repos:
    print("Didn't see repo. '%s'" % TAG_REPO)
    exit(10)

tag_repo = GH.get_repo("%s/%s" % (USER, TAG_REPO))

issues = {}
print("Reading issues")
for issue in tag_repo.get_issues():
    rawkey = issue.title.split(':')[0]
    if '|' in rawkey:
        key = tuple(rawkey.split('|'))
    else:
        key = (rawkey, USER)
    # print("%s -> %s" % (rawkey, key))

    issues[key] = {'title': issue.title, 'body': issue.body, 'issue': issue}

for (repo, org) in repos:
    name = repo if org == USER else ("%s|%s" % (repo, org))
    title = "%s: %s" % (name, repos[(repo, org)]['desc'])
    body = URL_TEMPLATE % (org, repo)
    sleep = 0
    if (repo, org) not in issues:
        print("Creating issue for '%s'" % name)
        issue = tag_repo.create_issue(title, body=body)
        issue.add_to_labels("unclassified")
        sleep = RATE_LIMIT
    else:
        if issues[(repo, org)]['title'] != title:
            print("%s - update title" % name)
            issues[(repo, org)]['issue'].edit(title=title)
            sleep = RATE_LIMIT
        if issues[(repo, org)]['body'] != body:
            print("%s - update url" % name)
            issues[(repo, org)]['issue'].edit(body=body)
            sleep = RATE_LIMIT
    if sleep:
        print("Waiting %d seconds" % sleep)
        time.sleep(sleep)

for i in issues.values():
    del i['issue']
json.dump(
    {'repos': repos, 'issues': issues}, open("_last_run.json", 'w'), indent=4
)
