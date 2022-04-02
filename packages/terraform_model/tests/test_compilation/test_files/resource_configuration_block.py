"""
This is a basic Terraform model.
"""
from terraform_model.all import *
from terraform_model.blocks.configuration import Configuration


Resource(
    'sub-type',
    'name-str',
    config_block=Configuration(
        'config_block_sub_type',
        'name',
        property='value',
    ),
)
