# std
from typing import Optional as Opt

# internal
from terraform_model.utils.utils import get_class_name
from terraform_model.blocks.configuration import Configuration
from terraform_model.blocks.data import Data
from terraform_model.blocks.provider import Provider
from terraform_model.blocks.resource import Resource
from terraform_model.gen.code import Code
from terraform_model.gen.utils import create_init_method, add_attributes

# constants
CONFIGURATION_BLOCK_TYPE = 'configuration'
DATA_BLOCK_TYPE = 'data'
PROVIDER_BLOCK_TYPE = 'provider'
RESOURCE_BLOCK_TYPE = 'resource'

CONFIGURATION_PATH = f'{Configuration.__module__}.{Configuration.__qualname__}'
DATA_PATH = f'{Data.__module__}.{Data.__qualname__}'
PROVIDER_PATH = f'{Provider.__module__}.{Provider.__qualname__}'
RESOURCE_PATH = f'{Resource.__module__}.{Resource.__qualname__}'

TYPE_PATHS = {
    CONFIGURATION_BLOCK_TYPE: CONFIGURATION_PATH,
    DATA_BLOCK_TYPE: DATA_PATH,
    PROVIDER_BLOCK_TYPE: PROVIDER_PATH,
    RESOURCE_BLOCK_TYPE: RESOURCE_PATH,
}


def compile_block(name: str, schema: dict, code: Code, block_type: str):
    parent_class_path = TYPE_PATHS[block_type]
    class_ = code.class_(get_block_class_name(name, block_type), parent_class_path)
    block_schema = schema.get('block', {})
    block_types = block_schema.get('block_types', {})
    for sub_name, sub_block_type in block_types.items():
        compile_block(sub_name, sub_block_type, class_, CONFIGURATION_BLOCK_TYPE)
    create_init_method(class_, block_schema, name)
    add_attributes(class_, block_schema)


def get_block_class_name(block_name: str, block_type: Opt[str] = None) -> str:
    if block_type == DATA_BLOCK_TYPE:
        return f'Data{get_class_name(block_name)}'
    elif block_type == PROVIDER_BLOCK_TYPE:
        return f'Provider{get_class_name(block_name)}'
    else:
        return get_class_name(block_name)
