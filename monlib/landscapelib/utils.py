import yaml
import itertools

from collections import Counter

from typing import Type
from typing import Dict
from typing import List
from typing import Union


def filter_dict_key(d: Dict, filter_field: str) -> List[Dict]:
    r = []
    for e in d:
        r.append(e.get(filter_field))
    return r


def filter_dict_value(d: Dict, filter_field: str, value: str = None) -> List[Dict]:
    r = []
    for e in d:
        if e[filter_field] == value:
            r.append(e)
        else:
            continue
    return r


def chain_lists(*l: List) -> List:
    return itertools.chain(*l)


def count_dublicated(seq: List) -> Dict[str, int]:
    res = {}
    for i in seq:
        counter = seq.count(i)
        if counter > 1:
            res[i] = counter
        else:
            continue
    return res


def dublicated(seq: List)-> List: 
    return [k for k,v in Counter(seq).items() if v>1]


def compare_lists(*l: List) -> List:
    return set(l[0]) - set(l[1])


def extract_dict_values(l: Dict) -> Union[List, str]:
    values = list(l.values())
    if len(values) > 1:
        return values
    else:
        return values[0]


def values_from_list(dict_list: List[Dict]) -> List:
    values: List = []
    for di in dict_list:
        values.append(extract_dict_values(di))
    return list(itertools.chain(values))


def extract_dict_keys(l: Dict) -> Union[List, str]:
    keys = list(l.keys())
    if len(keys) > 1:
        return keys
    else:
        return keys[0]


def keys_from_list(dict_list: List[Dict]) -> List:
    keys: List = []
    for di in dict_list:
        keys.append(extract_dict_keys(di))
    return list(itertools.chain(keys))


def filter_keys_from_list(dict_list: List[Dict], filter_field: str) -> List:
    result: List = []
    for item in dict_list:
        result.append(item[filter_field])
    return result


def freeze_dict(d: Dict) -> Type[frozenset]:
    return {frozenset(row.items()) for row in d}


def read_yaml(path: str) -> Dict:
    with open(path, 'r') as f:
        conf = yaml.safe_load(f.read())
    return conf


def split_list(l: List) -> List[List[str]]:
    le: int = len(l)
    middle_index: int = le // 2
    firs_half: List = l[:middle_index]
    second_half: List = l[middle_index:]
    return firs_half, second_half
