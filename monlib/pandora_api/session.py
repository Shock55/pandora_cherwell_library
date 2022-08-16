import logging
import requests

from typing import List
from typing import Dict
from typing import Union
from typing import Any
from typing import Type

from . import exceptions


logger = logging.getLogger(__name__)


class Session(requests.Session):
    def __init__(self) -> None:
        super().__init__()
        self.headers = {'content-type': 'application/json'}

    def request(self, *args: Any, **kwargs: Any) -> None:
        try:
            response: str = super().request(*args, **kwargs)
            response.raise_for_status()
            return Response(response)
        except requests.HTTPError as e:
            logger.exception('bad response')
            raise exceptions.BadResponse(response) from e
        except requests.exceptions.RequestException as e:
            logger.exception("could not recive response")
            raise exceptions.NoResponse(e.request) from e


class Response:
    def __init__(self, response: str) -> None:
        self._resp: str = response

    @property
    def data(self) -> None:
        try:
            return self.json()['response']
        except ValueError as e:
            raise exceptions.InvalidJsonError(self._resp) from e
        except KeyError as e:
            try:
                return self.json()['payload']
            except KeyError:
                raise exceptions.MissingResponseError(self._resp) from e

    @property
    def errors(self):
        try:
            return self.json()['meta']['errors']
        except ValueError as e:
            raise exceptions.InvalidJsonError(self._resp) from e
        except KeyError as e:
            raise exceptions.MissingMetaError(self._resp) from e
