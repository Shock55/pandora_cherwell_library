import logging
import itertools

from dataclasses import dataclass

from utils import count_dublicated

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Type
from typing import Union


logger = logging.getLogger(__name__)


@dataclass
class SystemModul:
    fqdn: str
    agent_name: str
    data: Union[int, str]
    last_change: int


@dataclass
class SystemItem:
    fqdn: str
    type: str
    state: str
    id: int
    quit_mode: bool 


class SystemData:
    def __init__(self, data, fqdn) -> None:
        if len(data) == 1:
            self.data = data[0]
        else:
            self.data = data
        self._list_item_names()
        self.fqdn = fqdn
        self.table = {}
    
    def filter_field(self, field: str, split: bool = False, split_string: str = '.') -> List:
        r = []
        for e in self.data:
            if split:
                r.append(e.get(field).split(split_string)[0])
            else:
                r.append(e.get(field))
        return r

    def _check_fqdn(self, data):
        for i in self.fqdn:
            if data.find(i) == -1:
                return data

    def check_fqdn(self):
        self.table['empty_fqdn_counter'] = 0
        self.table['empty_fqdn_hosts'] = []
        item_names = self.filter_field('FQDN')
        for e in item_names:
            host = self._check_fqdn(e)
            if host:
                self.table['empty_fqdn_counter'] = self.table['empty_fqdn_counter'] + 1
                self.table['empty_fqdn_hosts'].append(host)
            else:
                continue

    def _list_item_names(self):
        self.item_names = [item for item in self.data]



@dataclass
class Policy:
    name: str
    modules: List[Dict[str, str]]

    def count_dublicated_modules(self):
        counter = count_dublicated(self.modules)
        if counter:
            return counter
        else:
            return False


class PolicyStore:
    def __init__(self, policy_data: List, name: str):
        self.name: str = name
        self.policy: List = policy_data
        self.dublicated_cache: Dict[str: Union[str, int]] = dict()
        self._analyze_policy_objs()
        self._list_policy_names()
        self._list_all_modules()
        logger.warning("Dublicated Policies: {}, System: {}.".format(self.dublicated_cache['dub_policies'], self.name))
        logger.warning("Dublicated Modules: {}, System: {}.".format(self.dublicated_cache['dub_modules'], self.name))
    
    def policy_modules(self, search_policy: str) -> Union[List, str]:
        for policy in self.policy:
            if policy.name == search_policy:
                self._check_dub(policy.name)
                return policy.modules

    def _check_dub(self, policy_name: str) -> None:
        try:
            for modul in self.dublicated_cache[policy_name]:
                logger.warning("Dublicated module {} from policy: {}, from system: {}.".format(modul, policy_name, self.name))
        except KeyError:
            return True

    def _analyze_policy_objs(self):
        self.dublicated_cache['dub_policies']: str = count_dublicated(self.policy)
        self.dublicated_cache['dub_modules']: Dict[str: int] = dict()
        for item in self.policy:
            if item.count_dublicated_modules():
                count: Dict[str: Union[int, str]] = item.count_dublicated_modules()
                self.dublicated_cache['dub_modules'][item.name] = count
            else:
                continue
    
    def _list_policy_names(self) -> None:
        self.policy_names = [item.name for item in self.policy]

    def _list_all_modules(self) -> None:
        modules = [item.modules for item in self.policy]
        self.modules = list(itertools.chain(*modules))
