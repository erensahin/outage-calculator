"""
Provides an easier access to credentials
"""
import json
from typing import Any, Dict


class CredentialManager:

    def __init__(self, credential_file: str = "../assets/credentials.json"):
        self._credential_file = credential_file
        self._credentials = self._read_credentials()

    def _read_credentials(self) -> Dict[str, Any]:
        """
        Reads credential file and returns its content as a dictionary

        :return: credentials
        :rtype: Dict[str, Any]
        """
        with open(self._credential_file, "r") as fp:
            return json.load(fp)

    def get_api_key(self) -> str:
        """
        :return: api key
        :rtype: str
        """
        try:
            return self._credentials["api_key"]
        except KeyError as exc:
            msg = (
                "'api_key' is required in credential file: "
                f"{self._credential_file}"
            )
            raise KeyError(msg) from exc

    def get_api_url(self) -> str:
        """
        :return: api url
        :rtype: str
        """
        try:
            return self._credentials["api_url"]
        except KeyError as exc:
            msg = (
                "'api_url' is required in credential file: "
                f"{self._credential_file}"
            )
            raise KeyError(msg) from exc
