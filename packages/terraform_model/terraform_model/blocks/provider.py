# std
from __future__ import annotations
from typing import Optional as Opt

# internal
from terraform_model.internal.tftype import TfJsonLike, TfJsonObject
from terraform_model.helpers.scope import Scope
from .block import Block


class Provider(Block):

    def __init__(self, sub_type: str, alias: Opt[str] = None, **kwargs: TfJsonLike):
        if alias:
            kwargs['alias'] = alias
        super().__init__(sub_type, None, **kwargs)

    @property
    def tf_name(self):
        if 'alias' in self.tf_data:
            return f'{self.tf_sub_type}.{self.tf_data["alias"]}'
        return self.tf_sub_type

    @classmethod
    def tf_type(cls):
        return Provider

    @classmethod
    def tf_type_name(cls):
        return 'provider'

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> TfJsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        model = {}
        for block in blocks:
            if block.tf_sub_type not in model:
                model[block.tf_sub_type] = []
            model[block.tf_sub_type].append(block.tf_json())
        return model
