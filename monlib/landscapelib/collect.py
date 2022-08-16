import logging
import itertools
import sqlalchemy as db

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Type

from dataclasses import dataclass

from database import Connection
from database import SessionBase

from objs import Policy
from objs import PolicyStore

from catalyst import PandoraCatalyst
from catalyst import CherwellCatalyst

from sqlalchemy import or_
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import join


logger = logging.getLogger(__name__)


class PandoraModul(PandoraCatalyst):
    def __init__(self, connection: Type[Connection]):
        super().__init__(connection)
        self.__dict__.update(self._mapping)
        self.agent: Type[MetaData] = self.__dict__['tagente']
        self.event: Type[MetaData] = self.__dict__['tevento']
        self.state: Type[MetaData] = self.__dict__['tagente_estado']
        self.modul: Type[MetaData] = self.__dict__['tagente_modulo']
        self.fqdn = ['EU','HCNET', 'biz']

    def get_modul(self, target_modul: str, target_data: [str, int]) -> List[Dict]:
        data = self._load_modul(target_modul, target_data)
        return self.normalize(data, 'modul', self.fqdn)

    def _load_modul(self, target_modul: str, target_data: [int, str], load_all_modules: bool = False) -> List[Dict]:
        query = self._session.query(
                self.agent,
                self.agent.c.nombre.label('agent_name'),
                self.event,
                self.state,
                self.state.c.timestamp.label('current_timestamp'),
                self.state.c.last_status_change.label('last_change'),
                self.modul,
                self.modul.c.nombre.label('modul_name')) \
                        .join(self.event, self.agent.c.id_agente == self.event.c.id_agente) \
                        .join(self.modul, self.agent.c.id_agente == self.modul.c.id_agente) \
                        .join(self.state, self.modul.c.id_agente_modulo == self.state.c.id_agente_modulo)
        
        if isinstance(target_data, int):
            return query.filter(self.modul.c.nombre == target_modul, self.state.c.datos == target_data) \
                    .group_by(self.agent.c.nombre).all()
        else:
            return query.filter(self.modul.c.nombre == target_modul, self.state.c.datos.like("%" + target_data + "%")) \
                    .group_by(self.agent.c.nombre).all()


class PandoraAgent(PandoraCatalyst):
    def __init__(self, connection: Type[Connection]):
        super().__init__(connection)
        self.__dict__.update(self._mapping)
        self.agent = self.__dict__['tagente']
        self.group = self.__dict__['tgrupo']
        self.policy_agents = self.__dict__['tpolicy_agents']
        self.policy = self.__dict__['tpolicies']
        self.fqdn = ['EU','HCNET', 'biz']

    def get_agent(self, agent_type) -> List[Dict[str, int]]:
            func = getattr(self, "_load_{}".format(agent_type))
            data = func()
            return self.normalize(data, agent_type, self.fqdn, 'agent')

    def _load_server(self) -> List[Dict]:
        return self._session.query(
                self.agent,
                self.agent.c.id_grupo.label('group'),
                self.agent.c.nombre.label('agent_name'),
                self.group,
                self.policy_agents) \
                        .join(self.policy_agents, self.agent.c.id_agente == self.policy_agents.c.id_agent) \
                        .join(self.group, self.agent.c.id_grupo == self.group.c.id_grupo) \
                        .filter(self.policy_agents.c.id_policy == 116).all()
    
    def _load_network(self):
        return self._session.query(
                self.policy,
                self.group.c.nombre.label('group'),
                self.agent,
                self.agent.c.nombre.label('agent_name')) \
                        .join(self.group, self.policy.c.id_group == self.group.c.id_grupo) \
                        .join(self.agent, self.group.c.id_grupo == self.agent.c.id_grupo) \
                        .filter(self.group.c.icon == 'network').all()


class CherwellItem(CherwellCatalyst):

    item_types = {
            'network': 'Network Device',
            'server': 'Server'}

    def __init__(self, connection: Type[Connection]):
        super().__init__(connection)
        self.__dict__.update(self._mapping)
        self.item = self.__dict__['cmdb_items']
        self.fqdn = ['EU', 'HCNET', 'biz']

    def get_item(self, item_type: str, check_singel_item: bool = False, item_name: str = None) -> Union[List[Dict], str]:
        if check_singel_item:
            data = self._check_item(item_name, item_type)
        else:
            func = getattr(self, "_load_{}_item".format(item_type))
            data = func(item_type)
        return self._normalize_item(data, item_type, self.fqdn)
 
    def _check_item(self, item_name: str, item_type: str) -> List[Dict]:
        return self._session.query(
                self.item) \
                        .filter(self.item.c.FQDN.like("%" + item_name + "%")).all()

    def _load_network_item(self, item_type: str) -> List[Dict]:
        return self._session.query(self.item) \
                .filter(self.item.c.ConfigurationItemTypeName == CherwellItem.item_types[item_type], self.item.c.AssetType \
                .in_([
                    'Access Switch', 
                    'Datacenter Switch', 
                    'Router', 
                    'Patient Monitoring Switch', 
                    'Router']))


class PandoraPolicy(SessionBase):
    def __init__(self, connection: Type[Connection]):
        super().__init__(connection)
        self.__dict__.update(self._mapping)
        self.policy = self.__dict__['tpolicies']
        self.policy_modul =  self.__dict__['tpolicy_modules']

    def get_policy(self) -> List[Dict]:
        return PolicyStore(self._load_policy(), 'cherwell')
    
    def _load_policy(self):
        policy: List = []
        for name in self._load_policy_names():
            policy.append(Policy(name['policy_name'], filter_keys_from_list(self._session.query(
                self.policy_modul.c.name.label('modul_name')) \
                        .join(self.policy, self.policy_modul.c.id_policy == self.policy.c.id) \
                        .filter(self.policy.c.name == name['policy_name']).all(), 'modul_name')))
        return policy

    def _load_policy_names(self):
        return self._session.query(self.policy.c.name.label('policy_name')).group_by(self.policy.c.name).all()
                

class CherwellPolicy(SessionBase):
    def __init__(self, connection: Type[Connection]):
        super().__init__(connection)
        self.__dict__.update(self._mapping)
        self.policy = self.__dict__['policy']

    def get_policy(self) -> List[Dict]:
        return PolicyStore(self._load_policy(), 'cherwell')

    def _load_policy(self):
        policy: List = []
        for name in self._load_policy_names():
            policy.append(Policy(name['policy_name'], filter_keys_from_list(self._session.query(self.policy.c.Module_Name.label('modul_name')) \
                    .filter(self.policy.c.Policy_Name == name['policy_name']).all(), 'modul_name')))
        return policy

    def _load_policy_names(self):
        return self._session.query(self.policy.c.Policy_Name.label('policy_name')).group_by(self.policy.c.Policy_Name).all()
