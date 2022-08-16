import logging

from typing import List
from typing import Dict

from fileshare import CheckShare
from confighandler import ConfigHandler


logger = logging.getLogger(__name__)


class Axenita:
    def __init__(self, user: str, passwd: str):
        self._user: str = user
        self._passwd: str = passwd
        self._smbshare: List = self._init_smb_share(self._user, self._passwd)

    def check_shares(self, share_pathes: List) -> Dict:
        report_unreachable: List = []
        for path in share_pathes:
            if len(self._smbshare.list_dir(path)) < 0:
                logger.error("Axenita path {} is not reachable".format(path))
                report_unreachable.append(path)
            else:
                logger.info("Axenita path {} is reachable".format(path))
        return report_unreachable

    def _init_smb_share(self, user, passwd):
        try:
            return CheckShare(user, passwd)
        except Exception:
            logger.error("Could not reach Axenita Network File Share")
