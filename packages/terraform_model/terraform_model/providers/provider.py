# std
from __future__ import annotations
import os

# internal
from ..utils.types import JsonObject
from terraform_model.providers.schema.provider_schema import ProviderSchema

# constants
PROVIDERS_DIR = 'providers'


class Provider:
    providers = {}

    def __init__(self, name: str, schema: JsonObject):
        self.name = name
        self.schema = ProviderSchema(name, schema)
        self.providers[name] = self

    @property
    def dir(self) -> str:
        return os.path.join(PROVIDERS_DIR, self.friendly_name)

    @property
    def friendly_name(self):
        return self.name.replace('.', '_')

    @classmethod
    def get_provider(cls, name: str) -> Provider:
        return cls.providers[name]

    @property
    def short_name(self):
        return self.name.split('/')[-1]
