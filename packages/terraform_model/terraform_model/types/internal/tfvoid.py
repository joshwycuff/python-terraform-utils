# std
from __future__ import annotations
from typing import Optional as Opt

# internal
from terraform_model.types.internal.tftype import TfType


class TfVoid(TfType):

    def __str__(self):
        return 'void'

    def __repr__(self):
        return 'void'

    @classmethod
    def type(cls) -> str:
        return 'void'

    @classmethod
    def new(cls, data: Opt = None) -> TfVoid:
        try:
            return void
        except:
            return cls(None)


def tfvoid(data: Opt = None) -> TfVoid:
    return TfVoid.new(data)


void = tfvoid()
