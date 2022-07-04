"""
Requester class abstracts all requests have been made and attachs anything
required (i.e. api key) to the request
"""
from urllib.parse import urljoin
from typing import Any, Dict, List, Union

import requests
from requests.adapters import HTTPAdapter, Retry


class Requester:

    def __init__(self, base_url: str, api_key: str, max_retries: int = 5):
        """
        :param base_url: Base API URL. (i.e. https://localhost:5000)
        :type base_url: str
        :param api_key: API key which is used for auth
        :type api_key: str
        :param max_retries: number of retries in case request faces with an
            unexpected response from the server. Defaults to 5
        :type max_retries: int
        """
        self._base_url = base_url
        self._api_key = api_key
        self._max_retries = max_retries

    def _get_headers(self) -> Dict[str, str]:
        """
        :return: request headers. Accept and X-API-Key
        :rtype: Dict[str, str]
        """
        return {
            "Accept": "application/json",
            "X-API-Key": self._api_key
        }

    def _handle_response(self, res: requests.Response) -> requests.Response:
        """
        Handles the API response and raises a `requests.exceptions.HTTPError`
        if status code of the response is not 200.

        :param res: response instance
        :type res: requests.Response
        :return: response when status code of the response is 200
        :rtype: requests.Response
        :raises: `requests.exceptions.HTTPError` if status code of the
            repsonse is not 200.
        """
        if res.status_code != 200:
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError as exc:
                msg = f"{exc} {res.json()}"
                raise requests.exceptions.HTTPError(msg) from exc

        return res

    def _get_request_session(self) -> requests.Session:
        """
        :return: request session instance
        :rtype: requests.Session
        """
        session = requests.Session()
        retries = Retry(
            total=self._max_retries,
            backoff_factor=0.1,
            status_forcelist=[500]
        )
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def get(
        self,
        endpoint: str,
        **params: Dict[str, Any]
    ) -> Union[List, Dict]:
        """
        Sends get requests to the given endpoint, and with optional params.

        :param endpoint: endpoint of the API to send the get request
        :type endpoint: str
        :param params: keyword arguments which will be used as query-string
            params. There will be no query-string param if no keyword-argument
            is specified. (i.e. sort=id, order=asc)
        :type params: Dict[str, Any]
        :return: response serialized to python list or dict
        :rtype: Union[List, Dict]
        """
        url = urljoin(self._base_url, endpoint)
        req_session = self._get_request_session()
        res = req_session.get(url, headers=self._get_headers(), params=params)
        res = self._handle_response(res)
        return res.json()

    def post(
        self,
        endpoint: str,
        body: Dict[Any, Any],
        **params: Dict[str, Any]
    ) -> Union[List, Dict]:
        """
        Sends post requests to the given endpoint and with the given body,
        if specified.

        :param endpoint: endpoint of the API to send the get request
        :type endpoint: str
        :param body: POST request body
        :type body: Dict[Any, Any]
        :param params: keyword arguments which will be used as query-string
            params. There will be no query-string param if no keyword-argument
            is specified. (i.e. sort=id, order=asc)
        :type params: Dict[str, Any]
        :return: response serialized to python list or dict
        :rtype: Union[List, Dict]
        """
        url = urljoin(self._base_url, endpoint)
        req_session = self._get_request_session()
        res = req_session.post(
            url, headers=self._get_headers(), json=body, params=params)
        res = self._handle_response(res)
        return res.json()
