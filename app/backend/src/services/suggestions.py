import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from openai import OpenAI
from core.config import settings
from prompts.prompt import Prompt
from text_extractor import TextExtractor
from schemas.models import Suggestions

def suggestions (cv_file: str) -> Suggestions:
    """Generate suggestions to improve a CV."""
    extractor = TextExtractor()
    cv_text = extractor.extract_text(cv_file)
    prompt = Prompt().suggestion(cv_text=cv_text)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # 1. Change .create() to .parse() and pass your Pydantic model to text_format
    response = client.responses.parse(
        model=settings.OPENAI_MODEL_SUGGESTIONS,
        temperature=settings.TEMPERATURE_SUGGESTIONS,
        max_output_tokens=settings.MAXIMUM_TOKENS_SUGGESTIONS,

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
        text_format=Suggestions,
    )

    # 2. Return the automatically validated and structured object directly
    return response.output_parsed

if __name__ == "__main__":
    # Example usage
    cv_file_path = r"C:\files\mrmayd\app\backend\files\ATS Anon Hossain BI.docx.pdf"
    suggestions_text = suggestions(cv_file=cv_file_path)
    suggestions_json_output = suggestions_text.model_dump_json(indent=4)
    print(suggestions_json_output)
    