import logging

from typing import Dict
from typing import List
from typing import Any
from typing import Optional
from typing import Type

from collect import PandoraModul
from collect import PandoraAgent
from collect import CherwellItem

from database import Connection
from database import SessionFactory


logger = logging.getLogger(__name__)


class CleanUp:
    
    def __init__(self, connection: List[Type[Connection]]):
        self._con: List[Type[Connection]] = connection
        self._item = CherwellItem(self._con['cherwell']) 
        self._agent = PandoraCritcalModul(self._con['pandora'])
        self.clean_up_list = []

    def modul(self, modul_name: str = None, modul_data: [int, str] = None) -> List[Dict]:
        modul = self._agent.get_modul(modul_name, modul_data)
        for sys_obj in modul.data:
            cher_host = self._item.get_item('Server', check_singel_item = True, item_name = sys_obj.get('FQDN'))
            lookup_table = dict()
            lookup_table['pandora_agent'] = sys_obj
            lookup_table['cherwell_ci'] = cher_host.data
            self.clean_up_list.append(lookup_table)
        return self.clean_up_list
