from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import (
    BaseChatModel,
)
from langchain_anthropic import ChatAnthropic
from app.config.settings import settings

from app.dto.linkedin_search_params_dto import LinkedInSearchParamsDto

def get_llm_model(model_type="openai") -> BaseChatModel:
    """
    Returns an LLM model based on the specified type.

    :param model_type: Type of the model to return. Options are "openai" or "anthropic".
    :return: An instance of the specified LLM model.
    """
    if model_type == "openai":
        model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    elif model_type == "anthropic":
        model = ChatAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            model="claude-3-haiku-20240307",
            temperature=0,
        )
    else:
        raise ValueError("Unsupported model type.")
    
    return model
