# std
import os
from pkg_resources import get_distribution


__version__ = get_distribution('terraform_install').version

if 'TERRAFORM_VERSION' in os.environ:
    __terraform_version__ = os.environ['TERRAFORM_VERSION']
elif os.path.isfile('.terraform-version'):
    with open('.terraform-version', 'r') as fh:
        __terraform_version__ = fh.read().strip()
elif os.path.isfile('.terraform_version'):
    with open('.terraform_version', 'r') as fh:
        __terraform_version__ = fh.read().strip()
else:
    try:
        from terraform_version import __version__ as __terraform_version__
    except ImportError:
        print('Could not determine Terraform version')
        exit(1)
