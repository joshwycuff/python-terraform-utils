# std
from inspect import Parameter
import re
from types import GenericAlias
from typing import Dict, List, Optional, Set, Union
import os

# internal
from terraform_model.utils.errors import TerraformTypeError
from terraform_model.internal.tftype import tftype, get_type_like
from terraform_model.internal.deferred import deferred
from terraform_model.gen.code import Class, SELF, Code
from terraform_model.expressions.expressions.getattr import GetAttr
from terraform_model.utils.utils import get_class_name
from terraform_model.types.internal.tfvoid import void

# constants
TERRAFORM_MODEL_USAGE = r'(terraform_model(\.\w+)*)\.(\w+)'
FORWARD_REF_PATTERN = r"ForwardRef\('(\w+)'\)"
GET_ATTR = f'{GetAttr.__module__}.{GetAttr.__qualname__}'


def convert_filepath_to_module_path(filepath: str) -> str:
    return os.path.splitext(filepath)[0].replace(os.path.sep, '.')


def class_path(cls: type) -> str:
    if _is_generic(cls):
        return _generic_class_path(cls)
    return f'{cls.__module__}.{cls.__name__}'


def _is_generic(cls: type) -> bool:
    return hasattr(cls, '__origin__') and hasattr(cls, '__args__')


def _generic_class_path(cls: type) -> str:
    origin = getattr(cls, '__origin__')
    args = getattr(cls, '__args__')
    return f'{class_path(origin)}[{", ".join(map(class_path, args))}]'


def create_init_method(class_: Class, block_schema: dict, sub_type: str):
    parameters = get_parameters(block_schema)
    method = class_.method('__init__', parameters)
    kwargs = 'dict(' + ', '.join((f'{p["name"]}={p["name"]}' for p in parameters)) + ')'
    method.append(f'super().__init__("{unsafe_name(sub_type)}", **{kwargs})')


def add_attributes(class_: Class, block_schema: dict):
    for name, schema in block_schema.get('attributes', {}).items():
        if schema.get('meta', False):
            continue
        return_annotation = tftype(schema.get('type', 'unknown'))
        _add_attribute(class_, name, return_annotation)


def _add_attribute(class_: Class, attribute_name: str, return_annotation: type):
    p = class_.property(attribute_name, annotation=return_annotation)
    p.append(f'return {class_path(return_annotation)}({GET_ATTR}({SELF}, "{attribute_name}"))')
    p.append('')


def get_parameters(block_schema: dict) -> list[dict]:
    parameters = []
    for name, attribute in block_schema.get('attributes', {}).items():
        if attribute.get('computed', False):
            continue
        parameter = {
            'name': name,
            'annotation': attribute.get('annotation') or get_annotation(attribute['type']),
        }
        if attribute.get('optional', False):
            parameter['default'] = void
        if attribute.get('kind') is not None:
            parameter['kind'] = attribute['kind']
        parameters.append(parameter)
    for name, block_type in block_schema.get('block_types', {}).items():
        parameter = {
            'name': name,
            'annotation': get_block_annotation(name, block_type),
        }
        if 'min_items' not in block_type:
            parameter['default'] = void
        parameters.append(parameter)
    return parameters


def is_str_list_type_definition(obj) -> bool:
    return (
            isinstance(obj, str)
            or (isinstance(obj, list) and obj[0] in ('list', 'map', 'set', 'object', 'tuple'))
    )


def get_type_from_str_list_type_definition(obj: Union[str, list[str]]):
    # list indicates a collection or structural type
    if isinstance(obj, list):
        # list indicates a collection or structural type
        collection_or_structural_type = get_type_from_str_list_type_definition(obj[0])
        if issubclass(collection_or_structural_type, deferred.TfCollectionFunction):
            return collection_or_structural_type[get_type_from_str_list_type_definition(obj[1])]
        if issubclass(collection_or_structural_type, deferred.TfStructural):
            raise NotImplementedError
        else:
            raise TerraformTypeError(
                f'{collection_or_structural_type} is not a collection or structure type')
    return {
        # primitives
        'bool': deferred.TfBool,
        'null': deferred.TfNull,
        'number': deferred.TfNumber,
        'string': deferred.TfString,
        # collections
        'list': deferred.TfList,
        'map': deferred.TfMap,
        'set': deferred.TfSet,
        # structurals
        'object': deferred.TfObject,
        'tuple': deferred.TfTuple,
        # unknown
        'unknown': deferred.TfUnknown,
    }.get(obj, deferred.TfUnknown)


def get_annotation(attribute_type: Union[str, list[str]]):
    if isinstance(attribute_type, str):
        return get_type_like(attribute_type)
    elif isinstance(attribute_type, list):
        if len(attribute_type) == 2:
            origin = get_type_like(attribute_type[0])
            origin_args = getattr(origin, '__args__')
            arg = get_type_like(attribute_type[1])
            arg_args = getattr(arg, '__args__')
            return Union[
                _generic_alias(origin_args[0], arg_args[0]),
                _generic_alias(origin_args[0], arg_args[1]),
                _generic_alias(origin_args[1], arg_args[0]),
                _generic_alias(origin_args[1], arg_args[1]),
            ]
        else:
            raise NotImplementedError
    else:
        raise NotImplementedError


def _generic_alias(origin, arg):
    if origin is Dict:
        return GenericAlias(origin, (str, arg))
    else:
        return GenericAlias(origin, (arg,))


def get_block_annotation(name: str, block_type: dict):
    class_name = get_class_name(name)
    nesting_mode = block_type.get('nesting_mode')
    annotation = class_name
    if nesting_mode == 'single':
        pass
    elif nesting_mode == 'list':
        annotation = Union[List[class_name], deferred.TfList[class_name]]
    elif nesting_mode == 'set':
        annotation = Union[Set[class_name], deferred.TfSet[class_name]]
    else:
        raise NotImplementedError
    min_items = block_type.get('min_items')
    if not min_items:
        annotation = Optional[annotation]
    return annotation


def remove_forward_refs(string: str) -> str:
    return re.sub(FORWARD_REF_PATTERN, r'\1', string)


def prepend_imports(code: str) -> str:
    terraform_model_imports = '\n'.join(set([
        f'from {m[0]} import {m[-1]}'
        for m in re.findall(TERRAFORM_MODEL_USAGE, code)
    ]))
    return f'''from typing import Dict, List, Optional, Union, Set, Tuple

import terraform_model
from terraform_model.types.internal.tfvoid import void

# types
NoneType = type(None)

{terraform_model_imports}


{code}
'''


def safe_name(name: str) -> str:
    return f'{name}_py_safe'


def unsafe_name(name: str) -> str:
    return name.replace('_py_safe', '')
