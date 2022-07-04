"""
Main process of retrieving, calculating, and sending outages
"""
import argparse
import logging
import sys
from typing import Dict, List

import dateutil.parser as dt_parser

from src.credential_manager import CredentialManager
from src.model import Device, Outage
from src.outage_service import OutageService
from src.requester import Requester

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
LOG = logging.getLogger(__name__)


def get_outage_service() -> OutageService:
    """
    :return: outage service instance
    :rtype: OutageService
    """
    credential_manager = CredentialManager("assets/credentials.json")
    api_url = credential_manager.get_api_url()
    api_key = credential_manager.get_api_key()
    requester = Requester(api_url, api_key)
    return OutageService(requester)


def filter_outages(
    outages: List[Outage],
    devices: List[Device],
    start_date: str
) -> List[Dict]:
    """
    Applies the filter to the outages to select corresponding outages.

    * Select outages that belong to devices of the site.
    * Select outages that begin after START_DATE

    :param outages: list of outages
    :type outages: List[Outage]
    :param devices: list of devices corresponding to the site
    :type devices: List[Devices]
    :param start_date: start date where outages should begin after this date
    :type start_date: str
    :return: List of outage body dictionaries
    :rtype: List[Dict]
    """
    valid_devices = {device.id: device.name for device in devices}
    return [
        {
            "id": outage.id,
            "name": valid_devices[outage.id],
            "begin": outage.begin,
            "end": outage.end
        }
        for outage in outages
        if outage.begin_datetime >= dt_parser.parse(start_date)
        and outage.id in valid_devices
    ]


def parse_args() -> argparse.Namespace:
    """
    :return: application arguments
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-id", default="norwich-pear-tree")
    parser.add_argument("--start-date", default="2022-01-01T00:00:00.000Z")
    known_args, _ = parser.parse_known_args()
    return known_args


def run() -> None:
    """
    Runs the main process:

    * Retrieves outages
    * Gets the site info of SITE_ID
    * Filters outages based on devices of the particular site and START_DATE
    * Attaches device name and posts the outages of SITE_ID
    """
    args = parse_args()
    site_id, start_date = args.site_id, args.start_date
    LOG.info("Start with arguments: %s", args)

    outage_service = get_outage_service()

    site_info = outage_service.get_site_info(site_id)
    LOG.info(
        "Retrieved site info of site %s. Number of devices: %s",
        site_id,
        len(site_info.devices)
    )

    outages = outage_service.get_outages()
    LOG.info("Retrieved %s outages", len(outages))

    outages = filter_outages(outages, site_info.devices, start_date)

    LOG.info("Posting %s outages for site %s", len(outages), site_id)
    outage_service.post_outages_to_site(site_id, outages)
    LOG.info("Posted successfully")


if __name__ == "__main__":
    run()
