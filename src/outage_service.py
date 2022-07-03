"""
Service that is responsible for communicating with Outage API
"""

from typing import Any, Dict, List

from .requester import Requester


class OutageService:

    def __init__(self, requester: Requester):
        """
        :param requester: requester instance to make API calls
        :type requester: Requester
        """
        self.requester = requester

    def get_outages(self) -> List[Dict[str, Any]]:
        """
        Retrieves outages from the Outage API and returns them

        :return: list of outages
        :rtype: List[Dict[str, Any]]
        """
        return self.requester.get("outages")

    def get_site_info(self, site_id: str) -> Dict[str, Any]:
        """
        Retrieves information of the specified site

        :param site_id: site identifier
        :type site_id: str
        :return: site information dictionary
        :rtype: Dict[str, Any]
        """
        return self.requester.get(f"site-info/{site_id}")

    def post_outages_to_site(
        self,
        site_id: str,
        outages: List
    ) -> Dict[str, Any]:
        """
        Posts outages of the specified site to the Outage API

        :param site_id: site identifier
        :type site_id: str
        :param outages: list of outages to post
        :type outages: List
        :return: site information dictionary
        :rtype: Dict[str, Any]
        """
        return self.requester.post(f"site-outages/{site_id}", outages)
