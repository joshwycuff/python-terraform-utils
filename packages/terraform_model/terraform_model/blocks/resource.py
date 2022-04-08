# std
from __future__ import annotations

# internal
from .block import Block
from terraform_model.internal.tftype import TfJsonLike
from terraform_model.types.primitives.tfstring import TfString


class Resource(Block):

    def __init__(self, sub_type: str, local_name: str, **kwargs: TfJsonLike):
        super().__init__(sub_type, local_name, **kwargs)

    def __rshift__(self, other: Resource):
        self.depends_on(other)

    def depends_on(self, other: Resource):
        if 'depends_on' not in self.tf_data:
            self.tf_data['depends_on'] = []
        self.tf_data['depends_on'].append(str(other))

    @classmethod
    def tf_type(cls):
        return Resource

    @classmethod
    def tf_type_name(cls):
        return 'resource'
