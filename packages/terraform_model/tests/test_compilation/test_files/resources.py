"""
This is a basic Terraform model.
"""
from terraform_model.all import *
from terraform_model.types.internal.tfvoid import void

Resource('sub-type', 'name-str', property='value')

Resource('sub-type-2', 'name-str-2', abc='def', void=void)
