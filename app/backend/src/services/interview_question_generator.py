import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from openai import OpenAI
from urllib import response 
from core.config import settings
from prompts.prompt import Prompt
from text_extractor import TextExtractor
from schemas.models import InterviewQuestionsResponse

def interview_question_generator(cv_file: str, jd_text: str, num_questions: int) -> InterviewQuestionsResponse:
    """Generate interview questions based on a CV."""
    extractor = TextExtractor()
    cv_text = extractor.extract_text(cv_file)
    prompt = Prompt().interview_questions_generator(cv_text=cv_text, jd_text=jd_text, num_questions=num_questions)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # 1. Change .create() to .parse() and pass your Pydantic model to text_format
    response = client.responses.parse(
        model=settings.OPENAI_MODEL_BASIC,
        temperature=settings.TEMPERATURE_BASIC,
        max_output_tokens=settings.MAXIMUM_TOKENS_BASIC,
        prompt_cache_retention="24h",
        prompt_cache_key="interview_question_id_123",

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
        text_format=InterviewQuestionsResponse,
    )

    # 2. Return the automatically validated and structured object directly

    # usage = response.usage
    # print(f"Input tokens: {usage.input_tokens}")
    # if hasattr(usage, "input_tokens_details") and usage.input_tokens_details and usage.input_tokens_details.cached_tokens:
    #     print(f"Cached tokens: {usage.input_tokens_details.cached_tokens}")
    # print(f"Output tokens: {usage.output_tokens}")
    # print(f"Total tokens: {usage.total_tokens}")

    return response.output_parsed

if __name__ == "__main__":
    # Example usage
    cv_file_path = r"C:\files\mrmayd\app\backend\files\ATS Anon Hossain BI.docx.pdf"
    jd_path = r"C:\files\mrmayd\app\backend\Dumy.txt"
    num_questions = 3  # Specify the number of interview questions you want to generate
    
    with open(jd_path, "r", encoding="utf-8") as file:
        jd_text = file.read()
    
    interview_question = interview_question_generator(cv_file=cv_file_path, 
                                                      jd_text=jd_text, 
                                                      num_questions=num_questions)
    
    interview_question_json_output = interview_question.model_dump_json(indent=4)
    print(interview_question_json_output)

