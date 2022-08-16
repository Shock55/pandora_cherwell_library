import logging

from typing import Dict
from typing import List
from utils import read_yaml


logger = logging.getLogger(__name__)


class ConfigHandler:
    def __init__(self):
        self._landscape = read_yaml('/etc/panodralib/landscape.yaml')
        self._pandora = self._landscape['pandora_connection']
        self._cherwell = self._landscape['cherwell_connection']

        self._monitoring = read_yaml('/etc/panodralib/monitoring.yaml')
        self._axenita = self._monitoring['axenita']

    def get_mon_cred(self, target: str) -> Dict:
        return self._monitoring[target]

    def get_db_conns(self):
        return [self._pandora, self._cherwell]

    def get_pan_con(self):
        return self._pandora

    def get_cher_con(self):
        return self._cherwell
