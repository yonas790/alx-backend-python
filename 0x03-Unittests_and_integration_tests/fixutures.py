#!/usr/bin/env python3

"""Fixtures for integration testing GithubOrgClient"""

org_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

repos_payload = [
    {"name": "episodes.dart", "license": {"key": "apache-2.0"}},
    {"name": "cpp-netlib", "license": {"key": "mit"}},
]

expected_repos = ["episodes.dart", "cpp-netlib"]
apache2_repos = ["episodes.dart"]
