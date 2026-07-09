import sys
import json
from pathlib import Path

# Fix path resolution to match your project architecture
sys.path.append(str(Path(__file__).resolve().parents[1]))

from openai import OpenAI
from core.config import settings
from prompts.prompt import Prompt
from text_extractor import TextExtractor
from schemas.models import InterviewEvaluationsResponse

def evaluate_interview(cv_file: str, input_json_path: str, output_json_path: str) -> InterviewEvaluationsResponse:
    """
    Reads the candidate's CV and the interview QA data, evaluates the responses 
    using OpenAI, and saves the final scored results along with an average score to a JSON file.
    """
    # 1. Extract CV text for candidate background reference
    extractor = TextExtractor()
    cv_text = extractor.extract_text(cv_file)
    
    # 2. Read the input interview questions, answers, and responses
    with open(input_json_path, "r", encoding="utf-8") as file:
        interview_json_data = file.read()
        
    # 3. Build the cache-optimized prompt
    prompt = Prompt().interview_evaluator(cv_text=cv_text, interview_json=interview_json_data)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    # 4. Request structured evaluation from OpenAI
    response = client.responses.parse(
        model=settings.OPENAI_MODEL_INTERVIEW_EVALUATION,
        max_output_tokens=settings.MAXIMUM_TOKENS_INTERVIEW_EVALUATION,
        prompt_cache_retention=settings.PROMPT_CACHE_RETENTION,
        reasoning=settings.REASONING_EFFORT,
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
        text_format=InterviewEvaluationsResponse,
    )
    
    # Simple token tracking metrics (with safe fallback for 0 cached tokens)
    usage = response.usage
    cached_tokens = usage.input_tokens_details.cached_tokens if (hasattr(usage, "input_tokens_details") and usage.input_tokens_details) else 0
    new_tokens = usage.input_tokens - cached_tokens
    
    print(f"Input tokens: {usage.input_tokens}")
    print(f"Cached tokens: {cached_tokens}")
    print(f"Output tokens: {usage.output_tokens}")
    print(f"Total tokens: {usage.total_tokens}")
    print(f"New tokens used: {new_tokens}")
    
    # 5. Extract the parsed Pydantic data object
    evaluated_data = response.output_parsed
    # --- MODIFICATION: Convert to dict and calculate deterministic average score ---
    output_dict = evaluated_data.model_dump()
    scores = [item.score for item in evaluated_data.evaluations]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    # Append the average score to the root of the output dictionary
    output_dict["avg_score"] = round(avg_score, 2)
    # -------------------------------------------------------------------------------
    
    # 6. Write the structured data with the avg_score included to the output JSON file
    with open(output_json_path, "w", encoding="utf-8") as file:
        json.dump(output_dict, file, indent=4)
        
    print(f"Successfully generated and saved evaluation report to: {output_json_path}")
    
    return evaluated_data

if __name__ == "__main__":
    # Define your local file paths
    cv_file_path = r"C:\files\mrmayd\app\backend\files\ATS Anon Hossain BI.docx.pdf"
    input_qa_json = r"app/backend/files/interview.json"
    output_result_json = r"app/backend/output/interview_result.json"
    
    # Run the evaluation pipeline
    evaluate_interview(
        cv_file=cv_file_path, 
        input_json_path=input_qa_json, 
        output_json_path=output_result_json
    )