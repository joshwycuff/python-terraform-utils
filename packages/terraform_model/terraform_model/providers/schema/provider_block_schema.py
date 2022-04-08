# std
from copy import deepcopy

# internal
from terraform_model.providers.schema.schema import SchemaABC
from terraform_model.providers.schema.meta_arguments.provider import PROVIDER_META_ARGUMENTS


class ProviderBlockSchema(SchemaABC):

    @property
    def schema(self):
        schema = deepcopy(self._schema)
        schema['block']['attributes'] = {
            **PROVIDER_META_ARGUMENTS['block']['attributes'],
            **schema['block'].get('attributes', {}),
        }
        schema['block']['block_types'] = {
            **PROVIDER_META_ARGUMENTS['block']['block_types'],
            **schema['block'].get('block_types', {}),
        }
        return schema
