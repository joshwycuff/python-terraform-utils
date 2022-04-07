# std
from __future__ import annotations
from inspect import Parameter
import json
from typing import Optional as Opt, Type, Union

# internal
from terraform_model.utils.types import JsonObject
from terraform_model.helpers.scope import Scope
from terraform_model.blocks.block import Block
from terraform_model.mixins import CompareMixin, HashableMixin, MathMixin
from terraform_model.types.internal.tftype import TfType
from terraform_model.types.conversions.typify import typify
from terraform_model.internal.tftype import tftype


class Variable(Block, CompareMixin, HashableMixin, MathMixin):

    def __init__(
            self,
            name: str,
            default: Opt[any] = None,
            type: Opt[Type[TfType]] = None,
            description: Opt[str] = None,
            **kwargs,
    ):
        if default is not None:
            kwargs['default'] = default
        if type is not None:
            kwargs['type'] = type
        if description is not None:
            kwargs['description'] = description
        super().__init__(None, name, **kwargs)

    def __str__(self):
        return f'var.{self.tf_name}'

    def __hash__(self):
        return hash(f'tfvariable-{self.tf_name}-{self.tf_data.get("default")}-{self.tf_data.get("type")}')

    @classmethod
    def tf_type(cls):
        return Variable

    @classmethod
    def tf_type_name(cls):
        return 'variable'

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> JsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        model = {}
        for block in blocks:
            model[block.tf_name] = block.tf_json()
        return model

    @classmethod
    def new(
            cls,
            name: str,
            default: Opt[any] = None,
            type: Opt[Type[TfType]] = None,
            description: Opt[str] = None,
            **kwargs,
    ) -> TfType:
        var = Variable(name, default=default, type=type, description=description, **kwargs)
        var = typify(var)
        return var

    @classmethod
    def from_parameter(cls, parameter: Parameter) -> TfType:
        name = parameter.name
        default = None if parameter.default is Parameter.empty else parameter.default
        _type = None if parameter.annotation is Parameter.empty else parameter.annotation
        return cls.new(name, default=default, type=_type)


def variable(
        name: str,
        default: Opt[any] = None,
        type: Opt[Union[str, Type[TfType]]] = None,
        description: Opt[str] = None,
        **kwargs,
):
    return Variable.new(name, default=default, type=type, description=description, **kwargs)
