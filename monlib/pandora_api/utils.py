import urllib
import logging

from .api import base

from typing import List
from typing import Any
from typing import Dict
from typing import Union
from typing import Type

from datetime import datetime
from datetime import timezone 
from datetime import timedelta


def urljoin(base: Any, path = None) -> str:
    if path is None:
        url = base
    else:
        if not base.endswith('/'):
            base += '/'
        url = urllib.parse.urljoin(base, str(path))
    return url
