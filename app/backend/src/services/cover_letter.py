#app/backend/src/cover_letter.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from openai import OpenAI
from core.config import settings
from prompts.prompt import Prompt
from text_extractor import TextExtractor
from schemas.models import CoverLetter

def cover_letter_generator(cv_file: str, jd_text: str) -> CoverLetter:
    """Generate a cover letter from a CV file and a job description."""

    extractor = TextExtractor()
    cv_text = extractor.extract_text(cv_file)
    prompt = Prompt().cover_letter(jd_text=jd_text, cv_text=cv_text)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # 1. Change .create() to .parse() and pass your Pydantic model to text_format
    response = client.responses.parse(
        model=settings.OPENAI_MODEL_COVER_LETTER,
        temperature=settings.TEMPERATURE_COVER_LETTER,
        max_output_tokens=settings.MAXIMUM_TOKENS_COVER_LETTER,

        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    }
                ],
            }
        ],
        text_format=CoverLetter,
    )

    # 2. Return the automatically validated and structured object directly
    return response.output_parsed


if __name__ == "__main__":
    # Example usage
    cv_file_path = "app/backend/files/ATS Anon Hossain BI.docx.pdf"
    job_description_path = r"C:\files\mrmayd\app\backend\Dumy.txt"

    with open(job_description_path, "r", encoding="utf-8") as file:
        job_description_text = file.read()

    cover_letter = cover_letter_generator(cv_file=cv_file_path, jd_text=job_description_text)
    json_cover_letter = cover_letter.model_dump_json(indent=4)
    print(json_cover_letter)
