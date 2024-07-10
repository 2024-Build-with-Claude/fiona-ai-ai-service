import json
import logging
import logging.config

import requests
from fastapi import APIRouter, Depends, Request
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.dependencies import get_db
from app.dto.resume_dto import (
    BasicProfile,
    EducationSection,
    ExperienceSection,
    SummarySection,
)
from app.services.message_service import create_message
from app.services.message_thread_service import (
    create_thread,
    get_thread_by_mufasa_ai_resume_id,
)


class ChatMessage(BaseModel):
    message: str


mufasa_ai_chat_controller = APIRouter()

simple_cache = {}


# get resume
def get_resume_from_mufasa_ai(headers: dict, mufasa_ai_resume_id: str) -> str:
    """Get resume from resume api"""
    logging.info(f"start get_resume_from_mufasa_ai: {mufasa_ai_resume_id}")

    url = f"{settings.MUFASA_AI_BASE_URL}/api/resume/{mufasa_ai_resume_id}"

    payload = {}

    response = requests.request(
        method="GET",
        url=url,
        headers=headers,
        data=payload,
    )

    logging.info(f"end get_resume_from_mufasa_ai: {response.text}")
    return response.text


@tool
def answer_question_from_resumeget_name(question: str) -> str:
    """Answer question from resume.

    Parameters:
        question (str): The question to answer

    Returns:
        str: the answer to the question
    """
    return question


@tool
def update_resume_experience_section(modification: str, request_id: str) -> str:
    """Update resume experience section
    if add the modification should include old experience section and new experience section
    if delete the modification should only include experience section no need to be deleted

    Parameters:
        modification (str): The modification result to the resume, the

    Returns:
        str: the updated resume
    """

    # structure the modification using LLM
    model = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0,
    )
    structured_llm = model.with_structured_output(schema=ExperienceSection)
    structured_result: ExperienceSection = structured_llm.invoke(input=modification)

    # get data from cache
    original_resume_data = simple_cache[request_id]["resume_data"]

    # modify the data
    original_resume_data["data"]["sections"]["experience"] = structured_result.dict()
    payload = json.dumps(original_resume_data)
    headers = {
        "Content-Type": "application/json",
        "Cookie": simple_cache[request_id]["cookie"],
    }
    resume_id = simple_cache[request_id]["resume_data"]["id"]
    url = settings.MUFASA_AI_BASE_URL + "/resume/" + resume_id
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response.text


@tool
def update_resume_education_section(modification: str, request_id: str) -> str:
    """Update resume education section
    if add the modification should include old education section and new education section
    if delete the modification should only include education section no need to be deleted

    Parameters:
        modification (str): The modification result to the resume

    Returns:
        str: the updated resume
    """

    # structure the modification using LLM
    model = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0,
    )
    structured_llm = model.with_structured_output(schema=EducationSection)
    structured_result: EducationSection = structured_llm.invoke(input=modification)

    # get data from cache
    original_resume_data = simple_cache[request_id]["resume_data"]

    # modify the data
    original_resume_data["data"]["sections"]["education"] = structured_result.dict()
    payload = json.dumps(original_resume_data)
    headers = {
        "Content-Type": "application/json",
        "Cookie": simple_cache[request_id]["cookie"],
    }
    resume_id = simple_cache[request_id]["resume_data"]["id"]
    url = settings.MUFASA_AI_BASE_URL + "/resume/" + resume_id
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response.text


@tool
def update_resume_summary_section(modification: str, request_id: str) -> str:
    """Update resume summary section
    The summary is like self introduction, it should be concise and to the point
    Please use the first person pronoun to write the summary

    Parameters:
        modification (str): The modification result to the resume

    Returns:
        str: the updated resume
    """

    # structure the modification using LLM
    model = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0,
    )
    structured_llm = model.with_structured_output(schema=SummarySection)
    structured_result: SummarySection = structured_llm.invoke(input=modification)

    # get data from cache
    original_resume_data = simple_cache[request_id]["resume_data"]

    # modify the data
    original_resume_data["data"]["sections"]["summary"] = structured_result.dict()
    payload = json.dumps(original_resume_data)
    headers = {
        "Content-Type": "application/json",
        "Cookie": simple_cache[request_id]["cookie"],
    }
    resume_id = simple_cache[request_id]["resume_data"]["id"]
    url = settings.MUFASA_AI_BASE_URL + "/resume/" + resume_id
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response.text


@tool
def update_resume_basics_section(modification: str, request_id: str) -> str:
    """Update resume basics section
    if add the modification should include old basics section and new basics section
    if delete the modification should only include basics section no need to be deleted

    Parameters:
        modification (str): The modification result to the resume

    Returns:
        str: the updated resume
    """

    # structure the modification using LLM
    model = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0,
    )
    structured_llm = model.with_structured_output(schema=BasicProfile)
    structured_result: BasicProfile = structured_llm.invoke(input=modification)

    # get data from cache
    original_resume_data = simple_cache[request_id]["resume_data"]

    # modify the data
    original_resume_data["data"]["basics"] = structured_result.dict()
    payload = json.dumps(original_resume_data)
    headers = {
        "Content-Type": "application/json",
        "Cookie": simple_cache[request_id]["cookie"],
    }
    resume_id = simple_cache[request_id]["resume_data"]["id"]
    url = settings.MUFASA_AI_BASE_URL + "/resume/" + resume_id
    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response.text


# upload resume
# @tool
# def update_resume(new_resume_data: str) -> str:
#     """Update resume to resume api

#     Parameters:
#         new_resume_data (str): The new resume data

#     Returns:
#         str: the new resume data
#     """

#     # parse the input to structure data

#     mufasa_ai_resume_id = ""
#     # update resume using API
#     url = f"https://resume-gpt-backend-production.up.railway.app/api/resume/{mufasa_ai_resume_id}"

#     payload = {}
#     headers = {
#         "Content-Type": "application/json",
#         # "Cookie": request.headers.get("Cookie", ""),
#     }

#     response = requests.request("PATCH", url, headers=headers, data=payload)

#     return response.text


@mufasa_ai_chat_controller.post("/{mufasa_ai_resume_id}/chats")
async def create_chat(
    request: Request,
    message: ChatMessage,
    mufasa_ai_resume_id: str,
    db_session: Session = Depends(get_db),
):
    """
    Create a chat
    """

    logging.info(f"start create_chat: Request ID: {request.state.request_id}")

    # check if resume id have message_thread instance, if not, create a new one
    thread_object = get_thread_by_mufasa_ai_resume_id(
        mufasa_ai_resume_id=mufasa_ai_resume_id, db_session=db_session
    )
    if thread_object is None:
        logging.info(
            f"No existing thread found, creating new thread for resume id {mufasa_ai_resume_id}"
        )
        thread_object = create_thread(
            mufasa_ai_resume_id=mufasa_ai_resume_id,
            db_session=db_session,
            platform="mufasa_ai",
        )
    tools = [
        # update_resume,
        answer_question_from_resumeget_name,
        update_resume_experience_section,
        update_resume_summary_section,
        update_resume_education_section,
        update_resume_basics_section,
    ]
    llm = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0,
    )
    prompt = hub.pull("hwchase17/openai-tools-agent")
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    # store request message in message DB
    request_message_object = create_message(
        message_thread_id=thread_object.id,
        sender="user",
        content=message.message,
        db_session=db_session,
    )

    # get resume data
    headers = {
        "Content-Type": "application/json",
        "Cookie": request.headers.get("Cookie", ""),
    }

    # get resume data from mufasa_ai
    resume_data = get_resume_from_mufasa_ai(
        headers=headers, mufasa_ai_resume_id=mufasa_ai_resume_id
    )

    # store resume data in cache
    simple_cache[request.state.request_id] = {}
    simple_cache[request.state.request_id]["resume_data"] = json.loads(resume_data)
    simple_cache[request.state.request_id]["cookie"] = request.headers.get("Cookie", "")

    # generate response using resume data

    # result = agent_executor.invoke({"input": "What is my experience"})
    question_data = {
        "input": "message:"
        + "\nrequest_id:"
        + request.state.request_id
        + "\n"
        + message.message
        + "\nresume:"
        + resume_data
        + "\ninstruction:reply with the answer to the user message, don't let user know the resume format is JSON",
    }
    result = agent_executor.invoke(question_data)

    # store response in DB
    response_message_object = create_message(
        message_thread_id=thread_object.id,
        sender="system",
        content=result["output"],
        db_session=db_session,
    )

    # delete simple cache
    del simple_cache[request.state.request_id]
    logging.info(f"end create_chat: {response_message_object.content}")
    return {"message": response_message_object.content}
