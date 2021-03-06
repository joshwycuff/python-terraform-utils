# internal
from terraform_model.internal.tftype import TfJsonLike
from terraform_model.types.internal.tftype import TfType
from terraform_model.types.conversions.typify import typify
from .block import Block


class Configuration(Block):

    def __init__(self, sub_type: str, **kwargs: TfJsonLike):
        super().__init__(sub_type, None, **kwargs)

    def __str__(self):
        return f'configuration.{self.tf_sub_type}.{self.tf_name}'

    @classmethod
    def tf_type(cls):
        return Configuration

    @classmethod
    def tf_type_name(cls):
        return 'configuration'

    @classmethod
    def new(cls, sub_type: str, name: str, **kwargs: TfJsonLike) -> TfType:
        return typify(Configuration(sub_type, name, **kwargs))


def configuration(sub_type: str, name: str, **kwargs: TfJsonLike):
    return Configuration.new(sub_type, name, **kwargs)
