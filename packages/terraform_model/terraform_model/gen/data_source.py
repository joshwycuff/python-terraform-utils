# std

# internal
from .code import Code
from . import utils
from terraform_model.gen.block import compile_block


# constants


def compile_data_source(name: str, data_source_schema: dict) -> str:
    code = Code()
    compile_block(name, data_source_schema, code, 'data')
    code.append('')
    return utils.prepend_imports(utils.remove_forward_refs(code.compile()))
