# std
from __future__ import annotations
import os

# internal
from terraform_model.internal.tftype import TfJsonLike, TfJsonObject
from terraform_model.helpers.scope import Scope
from .block import Block


class Module(Block):

    def __init__(self, name: str, source: str, **kwargs: TfJsonLike):
        data = {
            'source': source,
            **kwargs,
        }
        super().__init__(None, name, **data)

    def __str__(self):
        return f'module.{self.tf_name}'

    @classmethod
    def tf_type(cls):
        return Module

    @classmethod
    def tf_type_name(cls):
        return 'module'

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> TfJsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        model = {}
        for block in blocks:
            model[block.tf_name] = block.tf_json()
        return model


class NestedModule(Module):

    def __init__(self, nested_module_scope_dirpath: str, name: str, **kwargs: TfJsonLike):
        active_scope = Scope.get_active_scope()
        relpath = os.path.relpath(nested_module_scope_dirpath, active_scope.get_dirpath())
        source = os.path.sep.join(['.', relpath])
        data = {
            'source': source,
            **kwargs,
        }
        super().__init__(name, **data)
