# std
from copy import deepcopy

# internal
from terraform_model.providers.schema.schema import SchemaABC
from terraform_model.providers.schema.meta_arguments.resource import RESOURCE_META_ARGUMENTS


class ResourceSchema(SchemaABC):

    @property
    def schema(self):
        schema = deepcopy(self._schema)
        schema['block']['attributes'] = {
            **RESOURCE_META_ARGUMENTS,
            **schema['block']['attributes'],
        }
        return schema
