# std

# internal
import terraform_model.utils.utils
from .code import Code
from . import utils
from .utils import create_init_method, add_attributes
from terraform_model.blocks.resource import Resource
from terraform_model.blocks.configuration import Configuration


# constants
CONFIGURATION_PATH = f'{Configuration.__module__}.{Configuration.__qualname__}'
RESOURCE_PATH = f'{Resource.__module__}.{Resource.__qualname__}'


def compile_resource(name: str, resource_schema: dict) -> str:
    code = Code()
    _compile_block(name, resource_schema, code, 'resource')
    code.append('')
    return utils.prepend_imports(utils.remove_forward_refs(code.compile()))


def _compile_block(name: str, schema: dict, code: Code, block_type: str):
    class_name = terraform_model.utils.utils.get_class_name(name)
    class_ = code.class_(class_name, _get_parent_class_path(block_type))
    block_schema = schema.get('block', {})
    block_types = block_schema.get('block_types', {})
    for sub_name, sub_block_type in block_types.items():
        _compile_block(sub_name, sub_block_type, class_, 'configuration')
    create_init_method(class_, block_schema, name)
    add_attributes(class_, block_schema)


def _get_parent_class_path(block_type: str) -> str:
    if block_type == 'resource':
        return RESOURCE_PATH
    elif block_type == 'configuration':
        return CONFIGURATION_PATH
    else:
        raise NotImplementedError
