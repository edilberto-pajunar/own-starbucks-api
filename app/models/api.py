from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel

T = TypeVar("T")

class ApiResponse(GenericModel, Generic[T]):
    message: str
    data: Optional[T] = None