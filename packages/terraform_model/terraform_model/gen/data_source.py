# std

# internal
from .code import Code
from . import utils
from terraform_model.gen.block import compile_block


# constants


def compile_data_source(name: str, data_source_schema: dict) -> str:
    code = Code()
    compile_block(name, data_source_schema, code, 'data')
    # block_schema = data_source_schema.get('block', {})
    # class_name = _get_class_name(name)
    # class_ = code.class_(class_name, DATA_PATH)
    # create_init_method(class_, block_schema, name)
    # add_attributes(class_, block_schema)
    code.append('')
    return utils.prepend_imports(utils.remove_forward_refs(code.compile()))
