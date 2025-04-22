from io import BytesIO
from typing import Optional
from google import genai
import os


from pydantic import BaseModel
from streamlit.runtime.uploaded_file_manager import UploadedFile


class Transaction(BaseModel):
    date: str
    description: str
    withdraw: float
    deposit: float
    balance: Optional[float]


class Statement(BaseModel):
    bank_account: str
    bank_name: str
    bank_holder: str
    transactions: list[Transaction]


def process_file_with_gemini(
    file: UploadedFile, input_text: str, api_key: str
):
    # Configure the API key (set it as an environment variable or directly here)
    os.environ["GOOGLE_API_KEY"] = api_key
    # Initialize the Gemini model (using Gemini 1.5 Flash as an example)
    client = genai.Client(api_key=api_key)

    bytes_data = file.getvalue()
    myfile = client.files.upload(file=BytesIO(bytes_data), config={"mime_type": file.type})

    # Generate content from the input text
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[input_text, myfile],
        config={
            "response_mime_type": "application/json",
            "response_schema": Statement,
        },
    )

    output = response.text or "{}"

    # Return the generated text
    return output, response.usage_metadata
