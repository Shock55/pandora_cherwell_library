import os
import logging
import json
import base64
import urllib3
import yaml
import itertools
import sqlalchemy as db

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from sqlalchemy import or_
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.load_agents import LoadPandora
from lib.load_items import LoadCherwell


logger = logging.getLogger(__name__)

            
def adjustment_cherwell_pandora(controller: None) -> None:
    connection = controller.session_container['pandora']
    agent = connection.mapping.tables['tagente']
    session = connection.session
    
    for item in controller.data_container['cherwell']:
        for pandora_agent in controller.data_container['pandora']:
            
            if item.get('ID') == pandora_agent.get('ID'):
                if pandora_agent.get('FQDN') != item.get('FQDN'):
                    if item.get('FQDN') == '':
                        logger.error("cherwell item has no fqdn item: {}".format(item))
                        continue
                    else:
                        print(item)
                        session.query(agent).filter(
                                agent.c.id_agente == pandora_agent.get('ID')).update(
                                        {'nombre': item.get('FQDN'), 'alias': item.get('FQDN')})
            if item.get('STATE') == 'active' and item.get('QUIET_MODE') == False:
                if pandora_agent.get('QUIET_MODE') == True:
                    pass


def adjustment_pandora_cherwell(controller: None) -> None:
    pass


# not production ready
def set_ci_description(controller: None) -> None:
    for e in controller.data_container['cherwell']:
        print(e)


# not prodiction ready
def set_secondary_group(controller: None) -> None:
    for agent in controller.data_container['pandora']:
        for item in controller.data_container['cherwell']:
            if agent.get('ID') == item.get('ID'):
                hits = []
                hits.append(item.get('ID'))
        if len(hits) > 0:
            pass
            



def set_critical_instructions_disk_module(pan_engine: None) -> None:
    query = "update pandora.tagente_modulo set critical_instructions = 'Ein&#x20;Laufwerk&#x20;auf&#x20;dem&#x20;Server&#x20;hat&#x20;einen&#x20;Schwellwert&#x20;erreicht.&#x0d;&#x0a;Wir&#x20;bitten&#x20;Euch&#x20;dies&#x20;zu&#x20;bereinigen.&#x20;' where nombre like '%-Disk%' and critical_instructions = '';"
    logger.info(query)


def agent_save_mode(pan_engine: None) -> None:
    """Enables gloabl the operation save mode on the pandora agents."""
    """
    self.execute_query(self.pandora_engine, *[self.queries['operation_save_mode1'],
        self.queries['operation_save_mode2']])
    """
    query_1 = """update pandora.tagente
            join pandora.tagente_modulo on tagente.id_agente = tagente_modulo.id_agente
            set tagente.safe_mode_module = pandora.tagente_modulo.id_agente_modulo
            where tagente_modulo.nombre like '%HostAlive' and
                id_os = 9 and
                (id_grupo = 1 or
                    id_grupo = 13 or
                    id_grupo = 44 or
                    id_grupo = 52 or
                    id_grupo = 61 or
                    id_grupo = 62 or
                    id_grupo = 63 or
                    id_grupo = 64 or
                    id_grupo = 69 or
                    id_grupo = 73) and
                    safe_mode_module = 0;"""

    query_2 = """update pandora.tagente
            join pandora.tagente_modulo on tagente.id_agente = tagente_modulo.id_agente
            set tagente.safe_mode_module = pandora.tagente_modulo.id_agente_modulo
            where tagente_modulo.nombre like '%HostIPAlive'
            and id_os =7
            and safe_mode_module = 0;"""
    # execute_query
    # execute_query(query_1, query_2, pan_engine, operation = 'update')
    logger.info(query_1)
    logger.info(query_2)
