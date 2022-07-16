# std
import os

# internal
from terraform_install.version import __terraform_version__

TERRAFORM_UTILS_DIR = os.path.join(os.path.expanduser('~'), '.terraform-utils')
TERRAFORM_RELEASES_DIR = os.path.join(TERRAFORM_UTILS_DIR, 'releases')
TERRAFORM_PATH = os.path.join(TERRAFORM_RELEASES_DIR, __terraform_version__, 'terraform')
