# std
from __future__ import annotations

import keyword
from abc import ABC
from collections import defaultdict
from copy import deepcopy
from typing import Dict, Optional as Opt, Union

# internal
from terraform_model.utils.types import JsonObject
from terraform_model.utils.utils import get_class_name
from terraform_model.gen.utils import safe_name


class SchemaABC(ABC):
    _schemas: dict[str, list[SchemaABC]] = defaultdict(list)

    def __init__(self, name: str, schema: JsonObject):
        self._name = name
        self._schema = schema
        self._schemas[self.__class__.__name__].append(self)

    @property
    def name(self):
        return self._name

    @property
    def schema(self):
        return self._schema

    @property
    def safe_schema(self):
        safe_schema = deepcopy(self.schema)
        self._safe_schema(safe_schema)
        return safe_schema

    @staticmethod
    def _safe_schema(obj: Union[Dict, str], parent_key: Opt[str] = None):
        if isinstance(obj, dict):
            unsafe_keys = []
            for key in obj:
                if not is_name_safe(key, parent_key):
                    unsafe_keys.append(key)
                SchemaABC._safe_schema(obj[key], key)
            for unsafe_key in unsafe_keys:
                obj[safe_name(unsafe_key)] = obj.pop(unsafe_key)


def is_name_safe(name: str, parent_key: Opt[str] = None) -> bool:
    if parent_key == 'attributes':
        return not keyword.iskeyword(name)
    if parent_key == 'block_types':
        return not keyword.iskeyword(name) and not keyword.iskeyword(get_class_name(name))
    return True
