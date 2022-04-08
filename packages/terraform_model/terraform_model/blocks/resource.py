# std
from __future__ import annotations

# internal
from .block import Block
from terraform_model.internal.tftype import TfJsonObject, TfJsonLike
from terraform_model.types.internal.tfvoid import void


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

    def tf_json(self) -> TfJsonObject:
        obj = super().tf_json()
        if 'depends_on' in obj:
            obj['depends_on'] = [str(b) for b in obj['depends_on']]
        return obj

    @classmethod
    def tf_type(cls):
        return Resource

    @classmethod
    def tf_type_name(cls):
        return 'resource'
