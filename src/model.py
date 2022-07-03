"""
Request and response models
"""

from dataclasses import dataclass
from datetime import datetime
import dateutil.parser as dt_parser
from typing import Dict, Optional, List


@dataclass
class Outage:

    id: str
    begin: str
    end: str
    begin_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None

    @classmethod
    def from_dict(cls, outage_dict: Dict[str, str]):
        """
        Helper method to obtain Outage instance from a dictionary. Also,
        begin_datetime and end_datetime attributes are set.

        :param outage_dict: outage dictionary
        :type outage_dict: Dict[str, str]
        :return: Outage instance
        :rtype: Outage
        """
        outage = cls(**outage_dict)
        outage.begin_datetime = dt_parser.parse(outage.begin)
        outage.end_datetime = dt_parser.parse(outage.end)

        return outage


@dataclass
class Device:

    id: str
    name: str

    @classmethod
    def from_dict(cls, device_dict: Dict[str, str]):
        """
        Helper method to obtain Device instance from a dictionary

        :param device_dict: device dictionary
        :type device_dict: Dict[str, str]
        :return: Device instance
        :rtype: Device
        """
        return Device(**device_dict)


@dataclass
class SiteInfo:

    id: str
    name: str
    devices: List[Device]

    @classmethod
    def from_dict(cls, site_info_dict: Dict[str, str]):
        """
        Helper method to obtain SiteInfo instance from a dictionary.

        :param site_info_dict: site info dictionary
        :type site_info_dict: Dict[str, str]
        :return: SiteInfo instance
        :rtype: SiteInfo
        """
        devices = [
            Device.from_dict(device) for device in site_info_dict["devices"]]

        return cls(
            id=site_info_dict["id"],
            name=site_info_dict["name"],
            devices=devices
        )
