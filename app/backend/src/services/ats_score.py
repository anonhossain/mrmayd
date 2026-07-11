import sys
from pathlib import Path
from urllib import response
sys.path.append(str(Path(__file__).resolve().parents[1]))

from openai import OpenAI
from core.config import settings
from prompts.prompt import Prompt
from text_extractor import TextExtractor
from schemas.models import ATSScore

def ats_score(cv_file: str) -> ATSScore:
    """
    Calculate the ATS score for a CV.
    Returns a score between 0 and 1.
    """
    extractor = TextExtractor()
    cv_text = extractor.extract_text(cv_file)
    prompt = Prompt().ats_score(cv_text=cv_text)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # 1. Change .create() to .parse() and pass your Pydantic model to text_format
    response = client.responses.parse(
        model=settings.OPENAI_MODEL_BASIC,
        temperature=settings.TEMPERATURE_BASIC,
        max_output_tokens=settings.MAXIMUM_TOKENS_BASIC,
        prompt_cache_retention="24h",
        prompt_cache_key="ats_score_id_123",

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
        text_format=ATSScore,
    )

    # 2. Return the automatically validated and structured object directly
    return response.output_parsed

if __name__ == "__main__":
    # Example usage
    cv_file_path = r"C:\files\mrmayd\app\backend\files\ATS Anon Hossain BI.docx.pdf"
    ats_score_result = ats_score(cv_file=cv_file_path)
    ats_score_json_output = ats_score_result.model_dump_json(indent=4)
    print(ats_score_json_output)