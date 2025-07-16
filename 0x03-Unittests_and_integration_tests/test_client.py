#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


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
