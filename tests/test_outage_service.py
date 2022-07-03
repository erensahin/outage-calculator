"""
Unit tests for outage service
"""

import unittest
from unittest import mock

import requests

from src.outage_service import OutageService
from src.requester import Requester

MOCK_OUTAGES = [
    {"id": 1, "foo": "bar"},
    {"id": 2, "foo": "baz"},
]

MOCK_SITE_INFO = {
    "id": 1,
    "data": [
        {"foo", "bar"}
    ]
}


class TestOutageService(unittest.TestCase):

    @mock.patch("src.outage_service.Requester")
    def test_get_outages(self, mock_requester: Requester):
        """
        test get_outages method
        """
        mock_get = mock.MagicMock()
        mock_get.return_value = MOCK_OUTAGES
        mock_requester.get = mock_get

        outage_service = OutageService(mock_requester)
        outages = outage_service.get_outages()

        mock_get.assert_called_once_with("outages")
        self.assertListEqual(outages, MOCK_OUTAGES)

    @mock.patch("src.outage_service.Requester")
    def test_get_outages_failure(self, mock_requester: Requester):
        """
        test get_outages method in case of failure
        """
        mock_get = mock.MagicMock()
        mock_get.side_effect = requests.exceptions.HTTPError()
        mock_requester.get = mock_get

        outage_service = OutageService(mock_requester)
        with self.assertRaises(requests.exceptions.HTTPError):
            outage_service.get_outages()
            mock_get.assert_called_once_with("outages")

    @mock.patch("src.outage_service.Requester")
    def test_get_site_info(self, mock_requester: Requester):
        """
        test get_site_info method
        """
        mock_get = mock.MagicMock()
        mock_get.return_value = MOCK_SITE_INFO
        mock_requester.get = mock_get

        outage_service = OutageService(mock_requester)
        site_info = outage_service.get_site_info("my_site")

        mock_get.assert_called_once_with("site-info/my_site")
        self.assertDictEqual(site_info, MOCK_SITE_INFO)

    @mock.patch("src.outage_service.Requester")
    def test_get_site_info_failure(self, mock_requester: Requester):
        """
        test get_site_info method in case of failure
        """
        mock_get = mock.MagicMock()
        mock_get.side_effect = requests.exceptions.HTTPError()
        mock_requester.get = mock_get

        outage_service = OutageService(mock_requester)
        with self.assertRaises(requests.exceptions.HTTPError):
            outage_service.get_site_info("my_site")
            mock_get.assert_called_once_with("site-info/my_site")

    @mock.patch("src.outage_service.Requester")
    def test_post_outages_to_site(self, mock_requester: Requester):
        """
        test post_outages_to_site method
        """
        mock_post = mock.MagicMock()
        mock_requester.post = mock_post

        outage_service = OutageService(mock_requester)
        outage_service.post_outages_to_site("my_site", MOCK_OUTAGES)

        mock_post.assert_called_once_with("site-outages/my_site", MOCK_OUTAGES)

    @mock.patch("src.outage_service.Requester")
    def test_post_outages_to_site_failure(self, mock_requester: Requester):
        """
        test post_outages_to_site method in case of failure
        """
        mock_post = mock.MagicMock()
        mock_post.side_effect = requests.exceptions.HTTPError()
        mock_requester.post = mock_post

        outage_service = OutageService(mock_requester)
        with self.assertRaises(requests.exceptions.HTTPError):
            outage_service.post_outages_to_site("my_site", MOCK_OUTAGES)
            mock_post.assert_called_once_with(
                "site-outages/my_site", MOCK_OUTAGES)
