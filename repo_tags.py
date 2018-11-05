import os
import time

from getpass import getpass

from github import Github

LOGIN_INFO_FILE = "login.info"
TAG_REPO = "repo_tags"
RATE_LIMIT = 10  # wait seconds between creating issues
URL_TEMPLATE = "https://github.com/%s/%s"

if os.path.exists(LOGIN_INFO_FILE):
    USER, PWORD = open(LOGIN_INFO_FILE).read().split()
else:
    USER = input("Github username: ")
    PWORD = getpass()

GH = Github(USER, PWORD)

repos = {
    i.name: {'desc': i.description, 'url': i.url}
    for i in GH.get_user().get_repos()
}

if TAG_REPO not in repos:
    print("Didn't see repo. '%s'" % TAG_REPO)
    exit(10)

tag_repo = GH.get_repo("%s/%s" % (USER, TAG_REPO))

issues = {i.title.split(':')[0]: i.title for i in tag_repo.get_issues()}

for repo in repos:
    if repo not in issues:
        print("Creating issue for '%s'" % repo)
        issue = tag_repo.create_issue(
            "%s: %s" % (repo, repos[repo]['desc']),
            body=URL_TEMPLATE % (USER, repo),
        )
        issue.add_to_labels("unclassified")
        print("Waiting %d seconds" % RATE_LIMIT)
        time.sleep(RATE_LIMIT)
