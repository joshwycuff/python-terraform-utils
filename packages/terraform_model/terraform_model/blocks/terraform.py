# std
from typing import Optional as Opt

# external
from terraform_version import __version__

# internal
from terraform_model.utils.errors import TerraformModelException
from terraform_model.utils.types import Json, JsonObject
from terraform_model.helpers.scope import Scope
from .block import Block


class RequiredVersion(Block):

    def __init__(self, required_version: str = None):
        _required_version = required_version if required_version else __version__
        data = {'required_version': _required_version}
        super().__init__(None, 'RequiredVersion', **data)

    @classmethod
    def tf_type_name(cls):
        return 'RequiredVersion'

    @classmethod
    def tf_type(cls):
        return RequiredVersion

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> JsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        if len(blocks) > 1:
            raise TerraformModelException('Cannot have more than 1 RequiredVersion')
        if len(blocks) == 1:
            return blocks[0].tf_json()
        else:
            return {}


class Backend(Block):

    def __init__(self, backend_type: str, **kwargs: Json):
        super().__init__('backend', backend_type, **kwargs)

    @classmethod
    def tf_type_name(cls):
        return 'Backend'

    @classmethod
    def tf_type(cls):
        return Backend

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> JsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        _model = {}
        for block in blocks:
            _model[block.tf_name] = block.tf_json()
        return _model


class S3Backend(Backend):

    def __init__(self, region: str, bucket: str, key: str, **kwargs: Json):
        data = {
            'region': region,
            'bucket': bucket,
            'key': key,
            **kwargs
        }
        super().__init__('s3', **data)


class RequiredProvider(Block):

    def __init__(self, name: str, source: Opt[str] = None, version: Opt[str] = None):
        data = {}
        if source:
            data['source'] = source
        if version:
            data['version'] = version
        super().__init__('required_provider', name, **data)

    @classmethod
    def tf_type_name(cls):
        return 'RequiredProvider'

    @classmethod
    def tf_type(cls):
        return RequiredProvider

    @classmethod
    def tf_model(cls, scope: Scope[Block]) -> JsonObject:
        blocks = scope.get_items(cls.tf_type_name())
        _model = {}
        for block in blocks:
            _model[block.tf_name] = block.tf_json()
        return _model


class Terraform:

    @classmethod
    def types(cls):
        return ['RequiredVersion', 'Backend', 'RequiredProvider']

    @classmethod
    def model(cls, scope: Scope[Block]) -> JsonObject:
        _model = RequiredVersion.tf_model(scope)
        backend = Backend.tf_model(scope)
        if backend:
            _model['backend'] = backend
        required_providers = RequiredProvider.tf_model(scope)
        if required_providers:
            _model['required_providers'] = required_providers
        return _model
