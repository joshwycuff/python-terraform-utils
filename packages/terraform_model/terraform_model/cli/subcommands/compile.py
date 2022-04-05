# std
import os

# internal
from terraform_model.compilation.compile import import_module_from_filepath
from terraform_model.utils.logger import log
from terraform_model.model import compile_terraform
from terraform_model.cli.subcommands.terraform import validate


def compile_terraform_model(args):
    log.info(f'Compiling terraform model from file {args.filepath}')
    _validate(args)
    _ = import_module_from_filepath(args.filepath)
    compile_terraform()
    validate(args)


def _validate(args):
    if not os.path.isfile(args.filepath):
        log.error(f'File {args.filepath} does not exist')
        exit(1)
