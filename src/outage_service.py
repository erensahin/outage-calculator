"""
Service that is responsible for communicating with Outage API
"""

from typing import List

from .model import Outage, SiteInfo
from .requester import Requester


class OutageService:

    def __init__(self, requester: Requester):
        """
        :param requester: requester instance to make API calls
        :type requester: Requester
        """
        self.requester = requester

    def get_outages(self) -> List[Outage]:
        """
        Retrieves outages from the Outage API and returns them

        :return: list of outages
        :rtype: List[Outage]
        """
        outages = self.requester.get("outages")
        outages = [Outage.from_dict(outage) for outage in outages]
        return outages

    def get_site_info(self, site_id: str) -> SiteInfo:
        """
        Retrieves information of the specified site

        :param site_id: site identifier
        :type site_id: str
        :return: site information dictionary
        :rtype: SiteInfo
        """
        site_info = self.requester.get(f"site-info/{site_id}")
        return SiteInfo.from_dict(site_info)

    def post_outages_to_site(
        self,
        site_id: str,
        outages: List
    ) -> None:
        """
        Posts outages of the specified site to the Outage API

        :param site_id: site identifier
        :type site_id: str
        :param outages: list of outages to post
        :type outages: List
        :return: None
        :rtype: None
        """
        self.requester.post(f"site-outages/{site_id}", outages)
