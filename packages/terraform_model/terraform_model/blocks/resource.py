# std
from __future__ import annotations

# internal
from .block import Block
from terraform_model.internal.tftype import TfJsonObject, TfJsonLike, TfType
from terraform_model.types.internal.tfvoid import void
from terraform_model.expressions.expressions.getattr import GetAttr


class Resource(Block):

    def __init__(self, sub_type: str, local_name: str, **kwargs: TfJsonLike):
        super().__init__(sub_type, local_name, **kwargs)

    def __rshift__(self, other: Resource):
        other.depends_on(self)

    def depends_on(self, other: Resource):
        if 'depends_on' not in self.tf_data:
            self.tf_data['depends_on'] = []
        elif self.tf_data['depends_on'] is void:
            self.tf_data['depends_on'] = []
        self.tf_data['depends_on'].append(other)

    def ignore_changes(self, attribute):
        if 'lifecycle' not in self.tf_data or self.tf_data['lifecycle'] is void:
            self.tf_data['lifecycle'] = {}
        lifecycle = self.tf_data['lifecycle']
        if 'ignore_changes' not in lifecycle or lifecycle['ignore_changes'] is void:
            lifecycle['ignore_changes'] = []
        lifecycle['ignore_changes'].append(attribute)

    def tf_json(self) -> TfJsonObject:
        obj = super().tf_json()
        if 'depends_on' in obj:
            obj['depends_on'] = [str(b) for b in obj['depends_on']]
        lifecycle = obj.get('lifecycle', {})
        if 'ignore_changes' in lifecycle and isinstance(lifecycle['ignore_changes'], list):
            lifecycle['ignore_changes'] = [self._coerce_ignore_changes(b) for b in lifecycle['ignore_changes']]
        return obj

    @classmethod
    def tf_type(cls):
        return Resource

    @classmethod
    def tf_type_name(cls):
        return 'resource'

    @classmethod
    def _coerce_ignore_changes(cls, obj) -> str:
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, GetAttr):
            return cls._coerce_ignore_changes(obj.attr)
        elif isinstance(obj, TfType):
            return cls._coerce_ignore_changes(obj.data)
        else:
            return str(obj)
