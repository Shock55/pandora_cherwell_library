import logging
import smbclient

from typing import List


logger = logging.getLogger(__name__)


class CheckShare:
    def __init__(self, user, passwd):
        self.smb_con = smbclient
        self.smb_con.ClientConfig(username = user, password = passwd)

    def list_dir(self, path: str) -> List[str]:
        return self.smb_con.listdir(path)
