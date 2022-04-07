# std
from __future__ import annotations

# internal
from terraform_model.internal.tftype import TfJsonObject
from terraform_model.helpers.scope import Scope
from terraform_model.types.internal.tftype import TfType
from terraform_model.types.conversions.typify import typify
from .block import Block


class Output(Block):

    def __init__(self, name: str, value):
        super().__init__(None, name, value=value)

    def __str__(self):
        return str(self.tf_data['value'])

    @classmethod
    def tf_type(cls):
        return Output

    @classmethod
    def tf_type_name(cls):
        return 'output'

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> TfJsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        model = {}
        for block in blocks:
            model[block.tf_name] = block.tf_json()
        return model

    @classmethod
    def new(cls, name: str, value) -> TfType:
        return typify(Output(name, value))


def output(name: str, value):
    return Output.new(name, value)
