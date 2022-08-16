import logging

from typing import List
from typing import Dict
from typing import Union
from typing import Any
from typing import Type

from pandora_api import utils


class Manager:
    
    base_url: str = 'https://chrzapp1173.eu.hcnet.biz/pandora_console/include/api.php?op={}&op2={}&other={}'
    cred_struct: Dict[str, str] = {
            'api_pass': '&apipass={}',
            'user': 'user={}',
            'passwd': 'pass={}'
        }

    def __init__(self, session: str, api_pass: str, user: str, passwd: str) -> None:
        self.session: str = session
        self._api_pass: str = api_pass
        self._user: str = user
        self._passwd: str = passwd

        self._creds: Dic[str, str] = {}
        self._load_params()
        self.url: str = Manager.base_url
        self.cred: str = self.build_url('&', **self._creds)

    def build_url(self, seperator: str, url: str = None, **payload: Dict[str, Union[str, int]]) -> str:
        if url is None:
            pan_params: str = seperator.join(str(val) for val in payload.values())
            return pan_params
        else:
            pan_params: str = seperator.join(str(val) for val in payload.values())
            return seperator.join([url, pan_params])
    
    def _join_cred(self, seperator: str, base_params: str) -> str:
        return seperator.join([base_params, self.cred])
    
    def _load_params(self):
        self._creds['api_pass']: Dict[str, str] = Manager.cred_struct['api_pass'].format(self._api_pass)
        self._creds['user']: Dict[str, str] = Manager.cred_struct['user'].format(self._user)
        self._creds['passwd']: Dict[str, str] = Manager.cred_struct['passwd'].format(self._passwd)
