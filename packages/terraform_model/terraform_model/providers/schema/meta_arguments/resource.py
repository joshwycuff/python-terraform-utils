# std
from inspect import Parameter
from typing import Union

# internal
from terraform_model.blocks.provider import Provider
from terraform_model.blocks.resource import Resource


RESOURCE_META_ARGUMENTS = {
    "version": "",
    "block": {
        "attributes": {
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
            "provider": {
                # terraform properties
                "type": "",
                "description": "",
                "description_kind": "plain",
                "optional": True,
                # internal properties
                "annotation": Provider,
                "kind": Parameter.KEYWORD_ONLY,
                "meta": True,
            },
        },
        "block_types": {
            "lifecycle": {
                "nesting_mode": "single",
                "block": {
                    "attributes": {
                        "create_before_destroy": {
                            # terraform properties
                            "type": "bool",
                            "description": "",
                            "description_kind": "plain",
                            "optional": True,
                            # internal properties
                            "annotation": bool,
                            "kind": Parameter.KEYWORD_ONLY,
                            "meta": True,
                        },
                        "prevent_destroy": {
                            # terraform properties
                            "type": "bool",
                            "description": "",
                            "description_kind": "plain",
                            "optional": True,
                            # internal properties
                            "annotation": bool,
                            "kind": Parameter.KEYWORD_ONLY,
                            "meta": True,
                        },
                        "ignore_changes": {
                            # terraform properties
                            "type": "",
                            "description": "",
                            "description_kind": "plain",
                            "optional": True,
                            # internal properties
                            "annotation": Union[str, list[str]],
                            "kind": Parameter.KEYWORD_ONLY,
                            "meta": True,
                        }
                    }
                },
                # internal properties
                "kind": Parameter.KEYWORD_ONLY,
                "meta": True,
            },
        }
    },
}
