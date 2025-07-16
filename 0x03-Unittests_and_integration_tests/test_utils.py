#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map and related functions."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map."""

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError for invalid path."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        self.assertEqual(str(cm.exception), path[len(nested_map)])


class TestGetJson(unittest.TestCase):
    """Test the utils.get_json function ensuring correct output and proper mocking."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected payload and calls requests.get once."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator caches method calls correctly."""

    def test_memoize(self):
        """Test memoize decorator caches method call."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_obj = TestClass()

        with patch.object(
            test_obj,
            'a_method',
            wraps=test_obj.a_method
        ) as mocked_method:
            # Call a_property twice
            first_call = test_obj.a_property
            second_call = test_obj.a_property

            # The result must be correct
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)

            # a_method called only once due to memoization
            mocked_method.assert_called_once()
