# internal
from terraform_model.internal.tfstringify import tfstringify
from terraform_model.types.internal.tftype import TfType
from terraform_model.types.internal.tfunknown import TfUnknown
from terraform_model.mixins.getattr import GetAttrMixin
from terraform_model.mixins.expression import ExpressionMixin
from terraform_model.internal.tftype import is_generic


def tfjsonify(obj):
    if isinstance(obj, type) and issubclass(obj, TfType):
        return tfstringify(obj)
    elif is_generic(obj):
        return tfstringify(obj)
    elif hasattr(obj, 'json') and callable(obj.json):
        return tfjsonify(obj.json())
    elif (not isinstance(obj, GetAttrMixin) or isinstance(obj, TfUnknown)) and hasattr(obj, 'data'):
        return tfjsonify(obj.data)
    elif isinstance(obj, ExpressionMixin):
        return obj.expression()
    elif isinstance(obj, list):
        return [tfjsonify(element) for element in obj]
    elif isinstance(obj, dict):
        return {key: tfjsonify(value) for key, value in obj.items()}
    elif isinstance(obj, TfType):
        return tfjsonify(obj.data)
    elif isinstance(obj, set):
        return tfjsonify(list(obj))
    else:
        return obj
