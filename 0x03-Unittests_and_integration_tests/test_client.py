#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from unittest import TestCase


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct payload"""

        # Arrange: set the mock return value (mocked JSON response)
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act: create GithubOrgClient instance and access .org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: the mocked get_json called once with the expected URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        # The .org property returns the expected JSON payload
        self.assertEqual(result, expected_payload)


class TestGithubOrgClient(unittest.TestCase):
    # ... your existing tests ...

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the repos_url from org property"""

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

            client = GithubOrgClient("test-org")
            repos_url = client._public_repos_url

            self.assertEqual(
                repos_url,
                "https://api.github.com/orgs/test-org/repos"
            )


class TestGithubOrgClient(TestCase):
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names"""
        
        # Sample payload that get_json will return (list of repos)
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload
        
        # Mock the _public_repos_url property to a dummy URL
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"
            
            client = GithubOrgClient("test-org")
            repos = client.public_repos()
            
            # Assert the repo names returned match the names in the payload
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            
            # Assert the _public_repos_url property was accessed once
            mock_repos_url.assert_called_once()
            
            # Assert get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
