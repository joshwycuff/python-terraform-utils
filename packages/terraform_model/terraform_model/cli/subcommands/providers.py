# std
import os
import re
import shutil

# internal
from terraform_model.utils import log
from terraform_model.providers.load import load_provider_schemas
from terraform_model.providers.generate import generate_providers
from terraform_model.cli.subcommands.terraform import get_terraform
from terraform_model.utils.open import Open
from terraform_model.model import PROVIDERS
from terraform_model.compilation.compile import import_module_from_filepath
from terraform_model.model import compile_terraform

# constants
PATTERN = r'^\s*RequiredProvider\(.*\)'
REQUIRED_PROVIDERS_PY = os.path.join(PROVIDERS, 'required_providers.py')


def get_providers(args):
    log.info('Generating Terraform providers')
    if args.clean and os.path.isdir(PROVIDERS):
        log.debug(f'Cleaning up {PROVIDERS} directory')
        shutil.rmtree(PROVIDERS)
    required_providers = _get_required_providers(args.filepath)
    _write_required_providers_file(required_providers)
    _ = import_module_from_filepath(REQUIRED_PROVIDERS_PY)
    compile_terraform(dirpath=PROVIDERS)
    provider_schemas = _get_provider_schemas()
    providers = load_provider_schemas(provider_schemas)
    generate_providers(providers)


def _get_required_providers(filepath: str) -> list[str]:
    with open(filepath, 'r') as fh:
        content = fh.read()
    return re.findall(PATTERN, content, flags=re.MULTILINE)


def _write_required_providers_file(required_providers: list[str]):
    content = '\n'.join(
        ['from terraform_model.all import *']
        + ['']
        + required_providers
        + ['']
    )
    with Open(REQUIRED_PROVIDERS_PY, mode='w') as fh:
        fh.write(content)


def _get_provider_schemas():
    tf = get_terraform(cwd=PROVIDERS)
    tf.init()
    return tf.providers_schema(json=True, capture=True)
