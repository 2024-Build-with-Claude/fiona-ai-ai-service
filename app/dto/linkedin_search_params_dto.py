from langchain_core.pydantic_v1 import BaseModel, Field

from app.constants import CountryLiteral
from app.utils.list_utils import list_to_or_string


class LinkedInSearchParamsDto(BaseModel):
    """LinkedIn search params"""

    # title: str = Field(description="The title of the person you are looking for")
    # location: str = Field(description="The location of the person you are looking for")
    # active_experience: bool = Field(
    #     description="Whether the person has active experience"
    # )
    # keyword: str = Field(description="The keyword of the person you are looking for")

    experience_title: list[str] = Field(
        description="The title list of the person you are looking for",
        default=[],
    )
    country: list[CountryLiteral] = Field(
        description="""
        The country list of the person you are looking for, 
        if not specified, leave it empty list will search all countries
        """,
        default=[],
    )
    experience_company_name: str = Field(
        description="""
        The company name list of the person's experience,
        if not specified, leave it empty string will search all companies
        """,
        default="",
    )

    education_institution_name: str = Field(
        description="""
        The institution name list of the person's education,
        if not specified, leave it empty string will search all institutions
        """,
        default="",
    )

    location: str = Field(
        description="""
        The location (city) of the person you are looking for,
        if not specified, leave it empty string will search all locations
        """,
        default="",
    )

    keyword: list[str] = Field(
        description="The keyword list of the person you are looking for",
        default=[],
    )

    # effect is not good
    # summary: str = Field(
    #     description="""
    #     Search summary of the person you are looking for,
    #     if not specified, leave it empty string will search all summaries
    #     """
    # )

    def get_talent_pool_query_dict(self) -> dict:
        """
        Convert the LinkedIn search params to a query dictionary for the talent_pool service.
        """
        params_dict = self.dict()

        ###############################
        # list
        ###############################
        if params_dict.get("experience_title") == []:
            params_dict.pop("experience_title")
        if params_dict.get("country") == []:
            params_dict.pop("country")
        if params_dict.get("keyword") == []:
            params_dict.pop("keyword")

        # if list is empty, remove the query param
        params_dict["experience_title"] = list_to_or_string(
            params_dict.get("experience_title")
        )
        params_dict["country"] = list_to_or_string(params_dict.get("country"))
        params_dict["keyword"] = list_to_or_string(params_dict.get("keyword"))

        ###############################
        # string
        ###############################

        # if string is "", remove the query param
        if params_dict.get("experience_company_name") == "":
            params_dict.pop("experience_company_name")

        if params_dict.get("education_institution_name") == "":
            params_dict.pop("education_institution_name")

        # if params_dict.get("summary") == "":
        #     params_dict.pop("summary")

        if params_dict.get("location") == "":
            params_dict.pop("location")

        return params_dict