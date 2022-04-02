from terraform_model.types import *
from terraform_model.expressions.expressions.ternary import ternary
from terraform_model.functions import *

from terraform_model.blocks.terraform import RequiredVersion, RequiredProvider, Backend, S3Backend
from terraform_model.blocks.variable import variable
from terraform_model.blocks.data import data
from terraform_model.blocks.locals import local
from terraform_model.blocks.module import Module
from terraform_model.blocks.output import output
from terraform_model.blocks.resource import Resource
from terraform_model.blocks.provider import Provider

from terraform_model.decorators import module, module_function
from terraform_model.types.conversions.typify import typify
