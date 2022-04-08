# std
import os

# internal
import terraform_model.utils.utils
from terraform_model.utils import log
from terraform_model.providers.provider import Provider
from terraform_model.providers.schema.resource_schema import ResourceSchema
from terraform_model.gen.resource import compile_resource
from terraform_model.gen.data_source import compile_data_source
from terraform_model.gen import utils
from terraform_model.utils.open import Open
from terraform_model.gen.code import Code
from terraform_model.gen.block import compile_block, get_block_class_name, \
    DATA_BLOCK_TYPE, PROVIDER_BLOCK_TYPE


def generate_providers(providers: list[Provider]):
    for provider in providers:
        _generate_provider(provider)


def _generate_provider(provider: Provider):
    log.info(f'Generating provider {provider.name} at {provider.dir}')
    _generate_provider_class(provider)
    _generate_resources(provider.dir, provider.schema.resources)
    _generate_data_sources(provider.dir, provider.schema.data_sources)


def _generate_provider_class(provider: Provider):
    filepath = os.path.join(provider.dir, f'provider.py')
    log.debug(f'Generating provider {provider.name} at {filepath}')
    code = _compile_provider(provider.short_name, provider.schema.provider.safe_schema)
    utils.prepend_imports(code)
    with Open(filepath, mode='w') as fh:
        fh.write(code)
    _import_up(filepath, get_block_class_name(provider.short_name, PROVIDER_BLOCK_TYPE))


def _compile_provider(name: str, provider_block_schema: dict) -> str:
    code = Code()
    compile_block(name, provider_block_schema, code, PROVIDER_BLOCK_TYPE)
    code.append('')
    return utils.prepend_imports(utils.remove_forward_refs(code.compile()))


def _generate_resources(provider_dir: str, resource_schemas: list[ResourceSchema]):
    resources_dir = os.path.join(provider_dir, 'resources')
    for resource_schema in resource_schemas:
        _generate_resource(resources_dir, resource_schema)


def _generate_resource(resources_dir: str, resource_schema: ResourceSchema):
    filepath = os.path.join(resources_dir, f'{resource_schema.name}.py')
    log.debug(f'Generating resource {resource_schema.name} at {filepath}')
    code = compile_resource(resource_schema.name, resource_schema.safe_schema)
    utils.prepend_imports(code)
    with Open(filepath, mode='w') as fh:
        fh.write(code)
    _import_up(filepath, terraform_model.utils.utils.get_class_name(resource_schema.name))


def _generate_data_sources(provider_dir: str, data_source_schemas: list[ResourceSchema]):
    data_sources_dir = os.path.join(provider_dir, 'data_sources')
    for data_source_schema in data_source_schemas:
        _generate_data_source(data_sources_dir, data_source_schema)


def _generate_data_source(data_sources_dir: str, data_source_schema: ResourceSchema):
    filepath = os.path.join(data_sources_dir, f'{data_source_schema.name}.py')
    log.debug(f'Generating data source {data_source_schema.name} at {filepath}')
    code = compile_data_source(data_source_schema.name, data_source_schema.safe_schema)
    with Open(filepath, mode='w') as fh:
        fh.write(code)
    _import_up(filepath, get_block_class_name(data_source_schema.name, DATA_BLOCK_TYPE))


def _import_up(filepath: str, class_name: str):
    module_path = utils.convert_filepath_to_module_path(filepath)
    import_statement = f'from {module_path} import {class_name}\n'
    parts = []
    for part in filepath.split(os.path.sep)[:-1]:
        parts.append(part)
        init_filepath = os.path.join(os.path.join(*parts), '__init__.py')
        with Open(init_filepath, mode='a') as fh:
            fh.write(import_statement)
