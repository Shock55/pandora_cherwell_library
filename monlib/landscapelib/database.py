import abc
import logging
import sqlalchemy as db

from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Type

from sqlalchemy import or_
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, engine: None, session: None, mapping: None) -> None:
        self.session: Type[Session] = session
        self.engine: Type[create_engine] = engine
        self.mapping: Type[MetaData] = mapping

    def close_connection(self) -> None:
        self.session.close()


class SessionBase:
    def __init__(self, connection: Type[Connection]) -> None:
        self._connection: Type[Connection] = connection
        self._session: Type[Session] = self._connection.session
        try:
            self._mapping: Type[MetaData] = self._connection.mapping.tables
        except AttributeError:
            logger.info(self._connection)
            self._mapping: Type[MetaData] = self._connection.mapping


class EngineFactory:
    def __init__(self):
        self.engine_cache: Dict[str, Type[create_engine]] = {}

    def build_engine(self, **kwargs: Any) -> Type[create_engine]:
        mssql: str = 'mssql+pymssql:'
        mysql: str = 'mysql+pymysql:' 
        if kwargs['database_system'] == 'mysql':
            base_con = mysql
        elif kwargs['database_system'] == 'mssql':
            base_con = mssql
        con_string: str = '//'.join([base_con, "{}:{}@{}/{}".format(
            kwargs['user'],
            kwargs['passwd'],
            kwargs['host'],
            kwargs['database'])])

        engine = create_engine(con_string)
        self.engine_cache[kwargs['name']] = engine
        return engine


class SessionFactory(EngineFactory):
    def __init__(self):
        super().__init__()
        self.session_cache: Dict[str, Type[Connection]] = {}
    
    def map_database(self, engine: None, **kwargs: [str, bool]) -> Type[MetaData]: 
        metadata: Type[MetaData] = MetaData(bind = engine)
        db.MetaData.reflect(metadata)
        if 'views' in kwargs:
            return self._map_views(kwargs['target_table'], metadata)
        else:
            return metadata

    def connection(self, **landscape) -> Type[Connection]:
        engine: Type[create_engine] = self.build_engine(**landscape)
        mapping: Type[MetaData] = self.map_database(engine = engine, **landscape)
        session: Type[Session] = self._create_session(engine)
        current_con: Type[Connection] = Connection(engine, session, mapping)
        self.session_cache[landscape['name']]: Dict[str, Type[Connection]] = current_con
        return current_con
    
    def _create_session(self, engine: Type[create_engine]) -> Session:
        Session: Type[Session] = sessionmaker(bind = engine)
        session: Type[Session] = Session()
        return session
    
    def _map_views(self, views: List, metadata: None) -> Type[MetaData]:
        mapped_views: Dict[str, Type[MetaData]] = {}
        for k, v in views.items():
            mapped_views[k]: Dict[str, Type[Table]] = Table(v, metadata, autoload = True)
        return mapped_views


def open_connections(con: [List[Dict]]) -> Type[Connection]:
    factory: Type[SessionFactory] = SessionFactory()
    connect: Dict[str, Connection] = dict()
    for c in con:
        connect[c['name']]: Dict[str, Type[Connection]] = factory.connection(**c)
    if len(connect) > 1:
        return connect
    else:
        return connect[c['name']]


def execute_query(*query, engine: None = None, single_value = True, operation: str = 'select') -> List[Dict]:
    """
    Executes query. Sqlalchemy wrapper where does manage directly the session.

    Args:
        engine (None): Sql engine object
        query (str): Sql query

    Yield:
        Iterator: Query result
    """
    with engine.connect() as con:
        if operation == 'select':
            for q in query:
                results = []
                r = con.execute(q)
                for elem in r:
                    results.append(elem._asdict())
                if single_value:
                    try:
                        return results[0]
                    except IndexError:
                        return False
                else:
                    return results
        elif operation == 'update':
            for q in query:
                con.execute(q)
