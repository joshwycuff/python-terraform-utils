# std
from __future__ import annotations
from abc import ABC
from typing import Optional as Opt, Type

# internal
from terraform_model.mixins import ExpressionMixin, GetAttrMixin
from terraform_model.helpers.scope import Scope, DEFAULT_NAME
from terraform_model.types.conversions.typify import typify
from terraform_model.internal.tftype import is_type_or_generic, TfJsonObject
from terraform_model.types.internal.tfvoid import void


def maybe_typify(something):
    if is_type_or_generic(something):
        return something
    else:
        return typify(something)


class Block(ABC, ExpressionMixin, GetAttrMixin):
    _types: dict[str, Type[Block]] = {}

    def __init__(
            self,
            sub_type: Opt[str],
            name: Opt[str],
            **data,
    ):
        self._tf_sub_type: Opt[str] = sub_type
        self._tf_name: Opt[str] = name
        self._tf_data: dict = {k: maybe_typify(v) for k, v in data.items()}
        type_name = self.tf_type_name()
        if type_name not in self._types:
            self._types[type_name] = self.tf_type()
        self._tf_scope: Scope = self._register()

    def __str__(self):
        return f'{self.tf_sub_type}.{self.tf_name}'

    @property
    def tf_data(self):
        return self._tf_data

    @classmethod
    def tf_type_name(cls):
        raise NotImplementedError

    @classmethod
    def tf_type(cls):
        raise NotImplementedError

    @property
    def tf_sub_type(self):
        return self._tf_sub_type

    @property
    def tf_name(self):
        return self._tf_name

    @property
    def tf_scope(self):
        return self._tf_scope

    def tf_json(self) -> TfJsonObject:
        return {key: value for key, value in self._tf_data.items() if value is not void}

    def _register(self):
        scope = Scope.get_active_scope()
        scope.add(self, name=self.tf_name, key=self.tf_type_name())
        return scope

    @classmethod
    def tf_exists(cls, name: str) -> bool:
        scope = Scope.get_active_scope()
        return scope.item_exists(name=name, key=cls.tf_type_name())

    @classmethod
    def tf_get_type(cls, type_name: str) -> Type[Block]:
        return cls._types[type_name]

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> TfJsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        model = {}
        for block in blocks:
            if block.tf_sub_type not in model:
                model[block.tf_sub_type] = {}
            model[block.tf_sub_type][block.tf_name] = block.tf_json()
        return model


Scope[Block](DEFAULT_NAME).enter()
