# std
from inspect import Parameter

# internal
from terraform_model.blocks.resource import Resource


RESOURCE_META_ARGUMENTS = {
    "local_name": {
        # terraform properties
        "type": "string",
        "description": "",
        "description_kind": "plain",
        "optional": False,
        # internal properties
        "annotation": str,
        "kind": Parameter.POSITIONAL_ONLY,
        "meta": True,
    },
    "depends_on": {
        # terraform properties
        "type": "",
        "description": "",
        "description_kind": "plain",
        "optional": True,
        # internal properties
        "annotation": Resource,
        "kind": Parameter.KEYWORD_ONLY,
        "meta": True,
    },
}
