from app.infrastructure.schemas import PageableParamDTO


def get_pageable_param(page: int = 1, size: int = 50) -> PageableParamDTO:
    """
    Returns a PageableParamDTO object with the given page and size parameters.

    Args:
        page (int): The page number to retrieve.
        size (int): The number of items per page.

    Returns:
        PageableParamDTO: A DTO object containing the page and size parameters.
    """
    return PageableParamDTO(
        page=page,
        size=size,
    )
