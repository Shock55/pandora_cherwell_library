import logging

from typing import List
from typing import Dict
from typing import Union
from typing import Any
from typing import Type

from .api import agent
from .session import Session


class Client:
    def __init__(self, api_pass: str, user: str, passwd: str) -> None:
        self.session: Type[Session] = Session()
        self.agents: Type[agent.Agents] = agent.Agents(self.session, api_pass, user, passwd)
    
