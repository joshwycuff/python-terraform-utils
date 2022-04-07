# internal
from .block import compile_block
from .code import Code
from . import utils


def compile_resource(name: str, resource_schema: dict) -> str:
    code = Code()
    compile_block(name, resource_schema, code, 'resource')
    code.append('')
    return utils.prepend_imports(utils.remove_forward_refs(code.compile()))
