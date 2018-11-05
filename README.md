# GitHub Repository Tags

There are lots of [threads like this](https://github.com/isaacs/github/issues/302)
asking GitHub to provide tags for repositories to make managing
long lists of repositories easier.  So far it seems nothing has
happened, so here's a quick hack to let you use tags to manage
repositories.

The [small python program](./repo_tags.py) in this repository
uses the GitHub API to get a list of your repos. and add their
name, description, and URL, to a new repo., by default called 
`repo_tags`.  Initially each “issue” is tagged `unclassified`,
but you can tag them as you please, using regular issue tagging.

When re-run, `repo_tags.py` only creates issues for repos. that
weren't already covered by an issue.

## How to use

### Setup

```shell
virtualenv -p python36 venv
. venv/bin/activate
pip install -r requirements.txt
```
and then log in to GitHub and create a repository called `repo_tags`
to house the issues, it's fine to leave it empty.

### Running

```shell
python repo_tags.py
```

You can either put your username and password (and nothing else) in a
file called `login.info`, or `repo_tags.py` will ask you for them when
it's run.

For each issue it creates it pauses 10 seconds to avoid triggering
GitHub rate-limiting lockouts.  So it takes a long time to do the
initial import, but it doesn't need supervision, so you can just
leave it running.

## TODO:

  - [ ] handle organizations properly, currently mixed in
        with user repos. with bad urls
  - [ ] update description for existing repositories when
        the description changes

