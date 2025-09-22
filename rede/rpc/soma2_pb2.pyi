from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RequisicaoSoma2(_message.Message):
    __slots__ = ("a",)
    A_FIELD_NUMBER: _ClassVar[int]
    a: int
    def __init__(self, a: _Optional[int] = ...) -> None: ...

class RespostaSoma2(_message.Message):
    __slots__ = ("res",)
    RES_FIELD_NUMBER: _ClassVar[int]
    res: int
    def __init__(self, res: _Optional[int] = ...) -> None: ...
