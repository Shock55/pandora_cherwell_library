import logging

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Type

from collect import PandoraPolicy
from collect import CherwellPolicy
from collect import Policy
from collect import PolicyStore
from collect import PandoraAgent
from collect import CherwellItem

from utils import split_list
from database import Connection


logger = logging.getLogger(__name__)


class PolicySync:
    def __init__(self, connection: List[Type[Connection]]):
        self._con: List[Type[Connection]] = connection
        self._cher_policy: Type[CherwellPolicy] = CherwellPolicy(self._con['cherwell'])
        self._pan_policy: Type[PandoraPolicy] = PandoraPolicy(self._con['pandora'])
        
    def policy_adjustment(self) -> None:
        pandora: Type[PolicyStore] = self._pan_policy.get_policy()
        cherwell: Type[PolicyStore] = self._cher_policy.get_policy()
        for policy in pandora.policy_names:
            if policy in cherwell.policy_names:
                cher_modules = cherwell.policy_modules(policy)
                pandora_modules = pandora.policy_modules(policy) 
                # master -> pandora
                for modul in cher_modules:
                    logger.info("Delete module: {} on policy: {} on system: {}.".format(modul, policy, cherwell.name)) 
                for modul in pandora_modules:
                    logger.info("Add modul: {} on policy: {} on system: {}.".format(modul, policy, pandora.name))


class NetworkImport:
    def __init__(self, connection: List[Type[Connection]]):
        self._con: List[Type[Connection]] = connection
        self._pandora = PandoraAgent(self._con['pandora'])
        self._cherwell = CherwellItem(self._con['cherwell'])

    def import_devices(self, item_type: str):
        # master -> cherwell
        self.pan_devices = self._pandora.get_agent(item_type)
        self.cher_devices = self._cherwell.get_item(item_type)

        for device in self.cher_devices.item_names:
            try:
                if self.pan_devices.data[device]:
                    diff = self._compare(device)
                    self._adjust(device, diff)
            except KeyError:
                logger.warning("Create Device: {}, Type: {} in Panodra".format(device, item_type))

    def _adjust(self, device: str, diff: List[tuple]) -> None:
        if diff != None:
            logger.info("Update Pandora Device {} with Properties: {}".format(device, diff))
        else:
            pass

    def _compare(self, device: str) -> None:
        cin = self.pan_devices.data[device].__dict__.items() ^ self.cher_devices.data[device].__dict__.items()
        if cin:
            diff = split_list(list(cin))
            logger.warning("Difference in Item Properties. Device: {}".format(device))
            logger.warning("Pandora Deivce {} State: {}".format(device, diff[0]))
            logger.warning("Cherwell Device {} State: {}".format(device, diff[1]))
            return diff[1]
