# internal
from terraform_model.utils.utils import get_class_name
from terraform_model.blocks.configuration import Configuration
from terraform_model.blocks.data import Data
from terraform_model.blocks.resource import Resource
from terraform_model.gen.code import Code
from terraform_model.gen.utils import create_init_method, add_attributes

# constants
CONFIGURATION_PATH = f'{Configuration.__module__}.{Configuration.__qualname__}'
DATA_PATH = f'{Data.__module__}.{Data.__qualname__}'
RESOURCE_PATH = f'{Resource.__module__}.{Resource.__qualname__}'


def compile_block(name: str, schema: dict, code: Code, block_type: str):
    class_ = code.class_(_get_class_name(name, block_type), get_parent_class_path(block_type))
    block_schema = schema.get('block', {})
    block_types = block_schema.get('block_types', {})
    for sub_name, sub_block_type in block_types.items():
        compile_block(sub_name, sub_block_type, class_, 'configuration')
    create_init_method(class_, block_schema, name)
    add_attributes(class_, block_schema)


def get_parent_class_path(block_type: str) -> str:
    if block_type == 'configuration':
        return CONFIGURATION_PATH
    elif block_type == 'data':
        return DATA_PATH
    elif block_type == 'resource':
        return RESOURCE_PATH
    else:
        raise NotImplementedError


def _get_class_name(name: str, block_type: str) -> str:
    if block_type == 'data':
        return f'Data{get_class_name(name)}'
    else:
        return get_class_name(name)
