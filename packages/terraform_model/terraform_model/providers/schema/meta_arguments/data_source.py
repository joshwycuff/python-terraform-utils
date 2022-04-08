# std
from inspect import Parameter


DATA_SOURCE_META_ARGUMENTS = {
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
