import sys
from pathlib import Path
from urllib import response
sys.path.append(str(Path(__file__).resolve().parents[1]))

from openai import OpenAI
from core.config import settings
from prompts.prompt import Prompt
from text_extractor import TextExtractor
from schemas.models import Matcher

def matcher( cv_file: str, jd_text: str) -> Matcher:
    """
    Compare the CV text and job description text to determine how well they match.
    Returns a similarity score between 0 and 1.
    """
    extractor = TextExtractor()
    cv_text = extractor.extract_text(cv_file)
    prompt = Prompt().matcher(cv_text=cv_text, jd_text=jd_text)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # 1. Change .create() to .parse() and pass your Pydantic model to text_format
    response = client.responses.parse(
        model=settings.OPENAI_MODEL_BASIC,
        temperature=settings.TEMPERATURE_BASIC,
        max_output_tokens=settings.MAXIMUM_TOKENS_BASIC,
        prompt_cache_retention="24h",
        prompt_cache_key="matcher_id_123",

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
        text_format=Matcher,
    )

    # 2. Return the automatically validated and structured object directly

    # usage = response.usage
    # print(f"Input tokens: {usage.input_tokens}")
    # if hasattr(usage, "input_tokens_details") and usage.input_tokens_details and usage.input_tokens_details.cached_tokens:
    #     print(f"Cached tokens: {usage.input_tokens_details.cached_tokens}")
    # new_tokens = usage.input_tokens - usage.input_tokens_details.cached_tokens
    # print(f"Output tokens: {usage.output_tokens}")
    # print(f"Total tokens: {usage.total_tokens}")
    # print(f"New tokens used: {new_tokens}")

    return response.output_parsed


if __name__ == "__main__":
    # Example usage
    cv_file_path = r"C:\files\mrmayd\app\backend\files\Anon Hossain AI.docx.pdf"
    jd_path = r"C:\files\mrmayd\app\backend\Dumy.txt"
    with open(jd_path, "r", encoding="utf-8") as file:
        jd_text = file.read()

    matcher_score = matcher(cv_file=cv_file_path, jd_text=jd_text)
    #print(f"Matcher Score: {matcher_score}")

    matcher_score_json_output = matcher_score.model_dump_json(indent=4)
    print(matcher_score_json_output)
    