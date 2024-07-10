import pypdf
from langchain_anthropic import ChatAnthropic
from llama_parse import LlamaParse

from app.dto.resume_dto import RootModel


def extract_text_from_pdf_pypdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_pdf_llama_parse(pdf_path):
    parser = LlamaParse(
        api_key="llx-Z9D4rk6z9Oz7DsvBA7QWhC5dWQ1j3LJjo0kOQhdYqfCZhXF4",
        result_type="markdown",
        num_workers=4,
        verbose=True,
        language="en",
        # language="ch_tra",
    )
    documents = parser.load_data(pdf_path)
    print(documents)
    return documents[0].text if documents else ""




def process_pdf_resume(pdf_path):
    # extracted_text = extract_text_from_pdf_llama_parse(pdf_path)
    extracted_text = extract_text_from_pdf_pypdf(pdf_path=pdf_path)
    response = structured_llm.invoke(extracted_text)
    return response
