# std
from copy import deepcopy

# internal
from terraform_model.providers.schema.schema import SchemaABC
from terraform_model.providers.schema.meta_arguments.data_source import DATA_SOURCE_META_ARGUMENTS


class DataSourceSchema(SchemaABC):

    @property
    def schema(self):
        schema = deepcopy(self._schema)
        schema['block']['attributes'] = {
            **DATA_SOURCE_META_ARGUMENTS['block']['attributes'],
            **schema['block']['attributes'],
        }
        schema['block']['block_types'] = {
            **DATA_SOURCE_META_ARGUMENTS['block']['block_types'],
            **schema['block'].get('block_types', {}),
        }
        return schema
