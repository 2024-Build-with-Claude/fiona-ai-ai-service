from langchain_openai import ChatOpenAI

from app.dto.linkedin_search_params_dto import LinkedInSearchParamsDto
from app.services.llm_model_service import get_llm_model


def natural_language_to_structured_query(
    natural_language_query: str,
) -> LinkedInSearchParamsDto:
    """Use natural language query to create a structured query"""

    model :BaseChatModel= get_llm_model("anthropic")
    structured_llm = model.with_structured_output(LinkedInSearchParamsDto)

    structured_result = structured_llm.invoke(natural_language_query)

    return structured_result
