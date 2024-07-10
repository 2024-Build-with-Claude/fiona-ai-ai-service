from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageableParamDTO(BaseModel, frozen=True):
    """
    Data transfer object for pageable parameters.

    Attributes:
        page (int): The page number.
        size (int): The number of items per page.
    """

    page: int
    size: int

    @property
    def offset(self):
        offset = (self.page - 1) * self.size
        return offset

    @property
    def limit(self):
        return self.size


class PageableResultDTO(Generic[T], BaseModel):
    """
    A generic class representing a pageable result.

    Attributes:
        total (int): The total number of items in the result set.
        page (int): The current page number.
        size (int): The number of items per page.
        data (list[T]): The list of items in the current page.
    """

    total: int
    page: int
    size: int
    data: list[T]
