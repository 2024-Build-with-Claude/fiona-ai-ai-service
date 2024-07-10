import json
import os
import shutil
from pathlib import Path

import requests
from fastapi import APIRouter, File, Request, UploadFile, Depends
from fastapi.responses import JSONResponse
from langchain_anthropic import ChatAnthropic

from app.config.settings import settings
from app.dto.resume_dto import RootModel
from app.services.resume_structure_service import extract_text_from_pdf_pypdf

fiona_ai_resume_controller = APIRouter()


# extract the file from request
def extract_file_from_request(request: Request, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse(
            status_code=400, content={"message": "Only PDF files are allowed"}
        )

    # Create a temp directory if it doesn't exist
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    # Use only the filename, not the full path
    file_location = temp_dir / (file.filename or "default.pdf")

    # 保存上傳的 PDF 文件
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # 從 PDF 提取文本 (這裡需要實現 pdf_to_text 函數)
    extracted_text = extract_text_from_pdf_pypdf(pdf_path=str(file_location))

    # 刪除臨時文件
    os.remove(file_location)
    return extracted_text


@fiona_ai_resume_controller.post("")
async def upload_and_import_resume(request: Request, files: UploadFile = File(...)):
    extracted_text = extract_file_from_request(request, files)

    # import resume
    url = f"{settings.MUFASA_AI_BASE_URL}/api/resume/import"
    # structured model
    model = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0,
    )

    structured_llm = model.with_structured_output(RootModel)
    structured_resume: RootModel = structured_llm.invoke(input=extracted_text)

    headers = {
        "Content-Type": "application/json",
        "Cookie": request.headers.get("Cookie", ""),
    }

    response = requests.request(
        "POST", url, headers=headers, data=structured_resume.json()
    )
    return response.json()


@fiona_ai_resume_controller.post("/{fiona_ai_resume_id}/update")
def upload_and_update_resume(
    fiona_ai_resume_id: str,
    request: Request,
    file: UploadFile = File(...),
):
    extracted_text = extract_file_from_request(request, file)

    # import resume
    url = f"{settings.MUFASA_AI_BASE_URL}/api/resume/{fiona_ai_resume_id}"
    model = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0,
    )

    structured_llm = model.with_structured_output(RootModel)
    structured_resume: RootModel = structured_llm.invoke(input=extracted_text)

    headers = {
        "Content-Type": "application/json",
        "Cookie": request.headers.get("Cookie", ""),
    }

    response = requests.request(
        "PATCH", url, headers=headers, data=structured_resume.json()
    )
    return response.json()
