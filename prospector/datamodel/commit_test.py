# from dataclasses import asdict
from telnetlib import COM_PORT_OPTION
import pytest

from git.git import Git

from .commit import make_from_raw_commit


@pytest.fixture
def repository():
    repo = Git("https://github.com/apache/struts.git")
    repo.clone()
    return repo


def test_proprocess_commit(repository):

    repo = repository
    raw_commit = repo.get_commit("93f378809cc73c65c1d689a0e32ec440c52e7ce2")

    commit = make_from_raw_commit(raw_commit)

    assert commit.message.startswith(
        "Merge pull request #480 from apache/WW-5117-reorders-stack [WW-5117]"
    )

    assert "WW-5117" in commit.jira_refs.keys()
    assert "480" in commit.ghissue_refs.keys()
    assert commit.cve_refs == []


def test_proprocess_commit_set(repository):

    repo = repository
    commit_set = repo.get_commits(
        since="1615441712", until="1617441712", filter_files="*.java"
    )
    preprocessed_commits = []

    for commit_id in commit_set:
        raw_commit = repo.get_commit(commit_id)
        preprocessed_commits.append(make_from_raw_commit(raw_commit))

    assert len(preprocessed_commits) == len(commit_set)


def test_commit_ordering(repository):
    print("test")
    # DO SOMETHING
