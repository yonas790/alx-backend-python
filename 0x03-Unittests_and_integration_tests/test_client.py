#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from unittest import TestCase
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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


class TestGithubOrgClient(unittest.TestCase):

    # ... other test methods ...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean based on license key"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get"""
        cls.get_patcher = patch("requests.get")

        # Start patcher and store the mock
        cls.mock_get = cls.get_patcher.start()

        # Define the side effect of .json() depending on call order
        cls.mock_get.return_value = Mock()
        cls.mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct data"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL"""
        with patch.object(GithubOrgClient, 'org', new_callable=Mock) as mock_org:
            mock_org.return_value = {"repos_url": "http://fake-url.com/repos"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://fake-url.com/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Unit test public_repos method"""
        mock_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(GithubOrgClient, "_public_repos_url", return_value="mock_url"):
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("mock_url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct result"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
