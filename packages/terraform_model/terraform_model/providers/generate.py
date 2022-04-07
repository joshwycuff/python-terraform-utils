# std
import os

# internal
import terraform_model.utils.utils
from terraform_model.utils import log
from terraform_model.providers.provider import Provider
from terraform_model.providers.resource_schema import ResourceSchema
from terraform_model.gen.resource import compile_resource
from terraform_model.gen.data_source import compile_data_source
from terraform_model.gen import utils
from terraform_model.utils.open import Open

# constants
PROVIDERS_DIR = 'providers'


def generate_providers(providers: list[Provider]):
    for provider in providers:
        _generate_provider(provider)


def _generate_provider(provider: Provider):
    provider_dir = os.path.join(PROVIDERS_DIR, provider.friendly_name)
    log.info(f'Generating provider {provider.name} at {provider_dir}')
    _generate_resources(provider_dir, provider.schema.resources)
    _generate_data_sources(provider_dir, provider.schema.data_sources)


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
    _import_up(filepath, f'Data{terraform_model.utils.utils.get_class_name(data_source_schema.name)}')


def _import_up(filepath: str, class_name: str):
    module_path = utils.convert_filepath_to_module_path(filepath)
    import_statement = f'from {module_path} import {class_name}\n'
    parts = []
    for part in filepath.split(os.path.sep)[:-1]:
        parts.append(part)
        init_filepath = os.path.join(os.path.join(*parts), '__init__.py')
        with Open(init_filepath, mode='a') as fh:
            fh.write(import_statement)
