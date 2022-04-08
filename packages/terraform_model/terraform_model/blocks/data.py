# internal
from terraform_model.internal.tftype import TfJsonObject, TfJsonLike
from terraform_model.types.internal.tftype import TfType
from terraform_model.types.conversions.typify import typify
from .block import Block


class Data(Block):

    def __init__(self, sub_type: str, local_name: str, **kwargs: TfJsonLike):
        super().__init__(sub_type, local_name, **kwargs)

    def __str__(self):
        return f'data.{self.tf_sub_type}.{self.tf_name}'

    def tf_json(self) -> TfJsonObject:
        obj = super().tf_json()
        if 'depends_on' in obj:
            obj['depends_on'] = [str(b) for b in obj['depends_on']]
        return obj

    @classmethod
    def tf_type(cls):
        return Data

    @classmethod
    def tf_type_name(cls):
        return 'data'

    @classmethod
    def new(cls, sub_type: str, name: str, **kwargs: TfJsonLike) -> TfType:
        return typify(Data(sub_type, name, **kwargs))


def data(sub_type: str, name: str, **kwargs: TfJsonLike):
    return Data.new(sub_type, name, **kwargs)
