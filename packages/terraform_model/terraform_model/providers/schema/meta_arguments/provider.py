# std
from inspect import Parameter


PROVIDER_META_ARGUMENTS = {
    "version": "",
    "block": {
        "attributes": {
            "alias": {
                # terraform properties
                "type": "string",
                "description": "",
                "description_kind": "plain",
                "optional": True,
                # internal properties
                "kind": Parameter.POSITIONAL_OR_KEYWORD,
                "annotation": str,
            },
        },
        "block_types": {},
    }
}
