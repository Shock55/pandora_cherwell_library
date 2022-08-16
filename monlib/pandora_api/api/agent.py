import logging

from collections import namedtuple

from typing import List
from typing import Dict
from typing import Union
from typing import Any
from typing import Type

from . import base
from pandora_api import utils


class Agents(base.Manager):
    def __init__(self, session: str, api_pass: str, user: str, passwd: str) -> None:
        super().__init__(session, api_pass, user, passwd)

    def create(self,
            agent_alias: str = None,
            ip: str = None,
            id_parent: int = None,
            id_group: int = None,
            cascade_protection: int = None,
            cascase_protection_module: int = None,
            interval_sec: int = None,
            id_os: int = None,
            name_server: str = None,
            custom_id: int = None,
            learning_mode: int = None,
            disabled: int = None,
            description: str = None,
            alias_as_name: int = None) -> None:
        
        payload: Dict[str, Union[int, str]] = {
                'ip': ip,
                'id_parent': id_parent,
                'id_group': id_group,
                'cascade_protection': cascade_protection,
                'cascase_protection_module': cascase_protection_module,
                'interval_sec': interval_sec,
                'id_os': id_os,
                'name_server': name_server,
                'custom_id': custom_id,
                'learning_mode': learning_mode,
                'disabled': disabled,
                'description': description,
                'alias_as_name': alias_as_name,
                '&other_mode=url_encode_separator_': '&other_mode=url_encode_separator_'
            }

        base_params = self.build_url('|', self.url.format('set', 'new_agent', agent_alias), **payload)
        url = self._join_cred('|', base_params)
        self.session.post(url, verify = False)
