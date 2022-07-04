"""
Unit tests for credential_manager
"""

import unittest
from unittest import mock

from src.credential_manager import CredentialManager


class TestCredentialManager(unittest.TestCase):

    @mock.patch("src.credential_manager.json.load")
    @mock.patch("src.credential_manager.open")
    def test_credential_manager(self, mock_open, mock_json_load):
        """
        test that credential manager loads credentials

        not that open method is mocked even we don't set it a return_value
        for it. it is because we need to open a file stream to read json file
        """
        credentials = {"foo": "bar"}
        mock_json_load.return_value = credentials

        cm = CredentialManager()
        self.assertDictEqual(credentials, cm._credentials)

        cm = CredentialManager("different_file.json")
        self.assertDictEqual(credentials, cm._credentials)
        self.assertEqual("different_file.json", cm._credential_file)

    @mock.patch("src.credential_manager.json.load")
    @mock.patch("src.credential_manager.open")
    def test_get_api_key(self, mock_open, mock_json_load):
        """
        test that get_api_key method returns expected api key

        not that open method is mocked even we don't set it a return_value
        for it. it is because we need to open a file stream to read json file
        """
        credentials = {"api_key": "foo"}
        mock_json_load.return_value = credentials

        cm = CredentialManager()
        api_key = cm.get_api_key()
        self.assertEqual("foo", api_key)

    @mock.patch("src.credential_manager.json.load")
    @mock.patch("src.credential_manager.open")
    def test_get_api_key_failure(self, mock_open, mock_json_load):
        """
        test that get_api_key method fails to find `api_key` and raises
        `KeyError`

        not that open method is mocked even we don't set it a return_value
        for it. it is because we need to open a file stream to read json file
        """
        credentials = {"apii_key": "foo"}
        mock_json_load.return_value = credentials

        cm = CredentialManager()
        with self.assertRaises(KeyError) as exc:
            cm.get_api_key()

        self.assertIn(
            "'api_key' is required in credential file: ", str(exc.exception))

    @mock.patch("src.credential_manager.json.load")
    @mock.patch("src.credential_manager.open")
    def test_get_api_url(self, mock_open, mock_json_load):
        """
        test that get_api_url method returns expected api key

        not that open method is mocked even we don't set it a return_value
        for it. it is because we need to open a file stream to read json file
        """
        credentials = {"api_url": "foo"}
        mock_json_load.return_value = credentials

        cm = CredentialManager()
        api_url = cm.get_api_url()
        self.assertEqual("foo", api_url)

    @mock.patch("src.credential_manager.json.load")
    @mock.patch("src.credential_manager.open")
    def test_get_api_url_failure(self, mock_open, mock_json_load):
        """
        test that get_api_url method fails to find `api_url` and raises
        `KeyError`

        not that open method is mocked even we don't set it a return_value
        for it. it is because we need to open a file stream to read json file
        """
        credentials = {"apii_url": "foo"}
        mock_json_load.return_value = credentials

        cm = CredentialManager()
        with self.assertRaises(KeyError) as exc:
            cm.get_api_url()

        self.assertIn(
            "'api_url' is required in credential file: ", str(exc.exception))
