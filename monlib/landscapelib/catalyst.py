import logging
import sqlalchemy as db

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Type

from objs import SystemData
from objs import SystemItem
from objs import SystemModul

from utils import filter_dict_value
from utils import filter_dict_key

from collections.abc import Callable
from collections.abc import Iterable

from database import Connection
from database import SessionBase

from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)


class PandoraCatalyst(SessionBase):
    def __init__(self, connection: Type[Connection]):
        super().__init__(connection)    

    def normalize(self, data: List[Dict], agent_type: str, fqdn: str, catalyst: str) -> List[Dict]:
        func = getattr(self, "_normalize_{}".format(catalyst))
        return func(data, agent_type, fqdn)

    def _normalize_modul(self, data: List[Dict], fqdn: str) -> List[Dict]:
        modules = []
        for e in data:
            modul = SystemItem(
                    e.agent_name.lower(),
                    e.modul_name,
                    e.datos,
                    e.last_change)
            modules.append(modul)
        return SystemData(modules, fqdn)
    
    def _normalize_agent(self, data: List[Dict], agent_type: str, fqdn: str) -> Type[SystemData]:
        agents = {}
        for item in data:
            if item.group is not None:
                agent = SystemItem(
                        item.agent_name.lower(),
                        agent_type,
                        'Active',
                        item.id_agente,
                        self._quiet_mode(item))
            else:
                continue
            agents.update({agent.fqdn: agent})
        return SystemData(agents, fqdn)
    
    def _quiet_mode(self, agent: Dict) -> bool:
        if agent.quiet == 0:
            return False
        else:
            return True


class CherwellCatalyst(SessionBase):
    def __init__(self, connection: Type[Connection]):
        super().__init__(connection)

    def _normalize_item(self, data: List[Dict], item_type: str, fqdn: str) -> List[Dict]:
        items = {}
        for item in data:
            cher_item = SystemItem(
                    item.FQDN.lower(),
                    item_type,
                    self._state(item),
                    self._id(item),
                    self._quiet_mode(item))
            items.update({cher_item.fqdn: cher_item})
        return SystemData(items, fqdn)
    
    def _quiet_mode(self, item: Dict) -> bool:
        if item.Outage == 0:
            return False
        else:
            return True

    def _state(self, item: Dict) -> str:
        if item.AssetStatus == 'Active':
            return 'Active'
        else:
            return item.AssetStatus

    def _id(self, item: Dict) -> int:
        if item.ExternalID != '':
            try:
                return int(item.ExternalID)
            except Exception:
                return None
        else:
            return None 
