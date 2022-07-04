"""
Unit tests for requester
"""

import unittest
from unittest import mock

import requests

from src.requester import Requester

MOCK_DATA = [
    {"id": 1, "foo": "bar"},
    {"id": 2, "foo": "baz"},
]


class TestRequester(unittest.TestCase):

    @mock.patch("src.requester.requests.Session.get")
    def test_get(self, mock_get):
        """
        test get method of Requester
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_DATA

        requester = Requester("https://fooapi:3333", "some_api_key")
        response_data = requester.get("foo")

        mock_get.assert_called_once_with(
            "https://fooapi:3333/foo",
            headers={
                'Accept': 'application/json',
                'X-API-Key': 'some_api_key'
            },
            params={}
        )
        self.assertListEqual(response_data, MOCK_DATA)

    @mock.patch("src.requester.requests.Session.get")
    def test_get_with_query_params(self, mock_get):
        """
        test get method of Requester with query params
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_DATA

        requester = Requester("https://fooapi:3333", "some_api_key")
        response_data = requester.get("foo", order="asc", sort="id")

        mock_get.assert_called_once_with(
            "https://fooapi:3333/foo",
            headers={
                'Accept': 'application/json',
                'X-API-Key': 'some_api_key'
            },
            params={
                "order": "asc",
                "sort": "id"
            }
        )
        self.assertListEqual(response_data, MOCK_DATA)

    @mock.patch("src.requester.requests.Session.get")
    def test_get_with_path_params(self, mock_get):
        """
        test get method of Requester with path params
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_DATA

        requester = Requester("https://fooapi:3333", "some_api_key")
        response_data = requester.get("foo/2")

        mock_get.assert_called_once_with(
            "https://fooapi:3333/foo/2",
            headers={
                'Accept': 'application/json',
                'X-API-Key': 'some_api_key'
            },
            params={}
        )
        self.assertListEqual(response_data, MOCK_DATA)

    @mock.patch("src.requester.requests.Session.get")
    def test_get_failure(self, mock_get):
        """
        test get method of Requester having a failure
        """
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = None
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError())

        requester = Requester("https://fooapi:3333", "some_api_key")

        with self.assertRaises(requests.exceptions.HTTPError):
            requester.get("foo")
            mock_get.assert_called_once_with(
                "https://fooapi:3333/foo",
                headers={
                    'Accept': 'application/json',
                    'X-API-Key': 'some_api_key'
                },
                params={}
            )

    @mock.patch("src.requester.requests.Session.post")
    def test_post(self, mock_post):
        """
        test post method of Requester
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        requester = Requester("https://fooapi:3333", "some_api_key")
        response_data = requester.post("bar", [{"id": 1, "key": "3"}])

        mock_post.assert_called_once_with(
            "https://fooapi:3333/bar",
            headers={
                'Accept': 'application/json',
                'X-API-Key': 'some_api_key'
            },
            params={},
            json=[{"id": 1, "key": "3"}]
        )
        self.assertDictEqual(response_data, {})

    @mock.patch("src.requester.requests.Session.post")
    def test_post_with_empty_body(self, mock_post):
        """
        test post method of Requester with empty body
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        requester = Requester("https://fooapi:3333", "some_api_key")
        response_data = requester.post("bar", [])

        mock_post.assert_called_once_with(
            "https://fooapi:3333/bar",
            headers={
                'Accept': 'application/json',
                'X-API-Key': 'some_api_key'
            },
            params={},
            json=[]
        )
        self.assertDictEqual(response_data, {})

    @mock.patch("src.requester.requests.Session.post")
    def test_post_with_params(self, mock_post):
        """
        test post method of Requester with query params
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        requester = Requester("https://fooapi:3333", "some_api_key")
        response_data = requester.post(
            "bar", [{"id": 1, "key": "3"}], order="asc", sort="id")

        mock_post.assert_called_once_with(
            "https://fooapi:3333/bar",
            headers={
                'Accept': 'application/json',
                'X-API-Key': 'some_api_key'
            },
            params={
                "order": "asc",
                "sort": "id"
            },
            json=[{"id": 1, "key": "3"}]
        )
        self.assertDictEqual(response_data, {})

    @mock.patch("src.requester.requests.Session.post")
    def test_post_with_path_params(self, mock_post):
        """
        test post method of Requester with path params
        """
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        requester = Requester("https://fooapi:3333", "some_api_key")
        response_data = requester.post("bar/2", [{"id": 1, "key": "3"}])

        mock_post.assert_called_once_with(
            "https://fooapi:3333/bar/2",
            headers={
                'Accept': 'application/json',
                'X-API-Key': 'some_api_key'
            },
            params={},
            json=[{"id": 1, "key": "3"}]
        )
        self.assertDictEqual(response_data, {})

    @mock.patch("src.requester.requests.Session.post")
    def test_post_failure(self, mock_post):
        """
        test post method of Requester having a failure
        """
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = None
        mock_post.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError())

        requester = Requester("https://fooapi:3333", "some_api_key")

        with self.assertRaises(requests.exceptions.HTTPError):
            requester.post("bar", [{"id": 1, "key": "3"}])
            mock_post.assert_called_once_with(
                "https://fooapi:3333/bar",
                headers={
                    'Accept': 'application/json',
                    'X-API-Key': 'some_api_key'
                },
                params={},
                json=[{"id": 1, "key": "3"}]
            )
