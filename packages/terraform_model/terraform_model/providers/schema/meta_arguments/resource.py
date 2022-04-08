# std
from inspect import Parameter


RESOURCE_META_ARGUMENTS = {
    "local_name": {
        # terraform properties
        "type": "string",
        "description": "",
        "description_kind": "plain",
        "optional": False,
        # internal properties
        "kind": Parameter.POSITIONAL_ONLY,
        "annotation": str,
    },
}
